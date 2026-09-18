import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import httpx
from config import config


class GitHubMonitor:
    """监控 CTNH-Modules 主仓库与全部子模块仓库的提交变化。"""

    def __init__(self):
        self.headers = {
            "Authorization": f"token {config.GITHUB_TOKEN}" if config.GITHUB_TOKEN else "",
            "Accept": "application/vnd.github.v3+json",
        }
        self.client = httpx.Client(headers=self.headers, timeout=30.0)

    def _load_state(self) -> Dict:
        try:
            with open(config.STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"repos": {}}

    def _save_state(self, state: Dict):
        os.makedirs(os.path.dirname(config.STATE_FILE), exist_ok=True)
        with open(config.STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=4, ensure_ascii=False)

    def _get_branch_head(self, repo: str, branch: str) -> Optional[str]:
        """获取分支最新 commit sha。"""
        url = f"https://api.github.com/repos/{repo}/commits/{branch}"
        try:
            resp = self.client.get(url, params={"per_page": 1})
            resp.raise_for_status()
            return resp.json().get("sha")
        except Exception as e:
            print(f"[monitor] 获取 {repo}@{branch} 分支头失败: {e}")
            return None

    def get_latest_commits_since(self, repo: str, branch: str, since_sha: str = "") -> List[Dict]:
        """获取自 since_sha 之后（不含）的所有 commits，旧->新。"""
        url = f"https://api.github.com/repos/{repo}/commits"
        params = {"sha": branch, "per_page": 100, "page": 1}
        new_commits: List[Dict] = []
        max_pages = 10
        while params["page"] <= max_pages:
            try:
                resp = self.client.get(url, params=params)
                resp.raise_for_status()
                commits = resp.json() or []
            except Exception as e:
                print(f"[monitor] 获取 {repo} commits 失败: {e}")
                break
            if not commits:
                break
            for commit in commits:
                if since_sha and commit.get("sha") == since_sha:
                    return new_commits
                new_commits.append(commit)
            params["page"] += 1
        return new_commits

    def get_commit_diff(self, repo: str, sha: str) -> str:
        url = f"https://api.github.com/repos/{repo}/commits/{sha}"
        try:
            resp = self.client.get(url, headers={**self.headers, "Accept": "application/vnd.github.v3.diff"})
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"[monitor] 获取 {repo} {sha[:7]} diff 失败: {e}")
            return ""

    def check_for_updates(self, force_latest: bool = False):
        """
        检查主仓库与所有子模块的新提交。
        返回 (changes, new_state)：
          changes: [{module, repo, branch, commits: [{sha, message, diff}]}]
        """
        state = self._load_state()
        repos = {"__main__": (config.MAIN_REPO, config.MAIN_BRANCH)}
        for module, (repo, branch) in config.SUBMODULES.items():
            repos[module] = (repo, branch)

        changes = []
        new_state = {"repos": dict(state.get("repos", {}))}

        for module, (repo, branch) in repos.items():
            head = self._get_branch_head(repo, branch)
            if not head:
                continue
            last_sha = state.get("repos", {}).get(module, {}).get("last_sha")

            if last_sha:
                # 有水位就一律按水位比对，force_latest 也不例外。
                # 曾经这里写成 `if force_latest or not last_sha`：只要手动触发（force_latest=true）
                # 就改走「最近 LOOKBACK 小时」的时间窗，于是任何早于 24 小时的未同步提交
                # 都会被判成「无新提交」。实测 CTNH-Mana 的 6890fd1 已积压 96.9 小时，
                # 手动重跑因此直接空跑（run #733），而这恰恰是最需要用重跑去补救的场景。
                commits = self.get_latest_commits_since(repo, branch, since_sha=last_sha)
                if force_latest and not commits and head != last_sha:
                    # 兜底：水位比对拿不到结果（例如 since_sha 已不在该分支的历史里，
                    # rebase/force-push 之后常见），但分支头确实前进了。此时按「从最新往回取
                    # 到 LOOKBACK 上限」兜底，避免把真实变更永久判成无提交。
                    print(f"[monitor] {module} 水位 {last_sha[:7]} 不在 {branch} 历史中，改用时间窗兜底")
                    commits = self._force_lookback(repo, branch)
                    if commits:
                        commits = self._truncate_at_watermark(commits, last_sha)
            elif force_latest:
                # 首次且强制：只知道「最近有一批提交」，用时间窗限制洪流
                commits = self._force_lookback(repo, branch)
            else:
                # 首次但未强制：无从比对水位，取时间窗内的提交
                commits = self._force_lookback(repo, branch)

            if commits:
                commits = commits[:10]  # 限制单次处理数量
                new_state["repos"][module] = {"last_sha": commits[0].get("sha")}
                changes.append({
                    "module": module,
                    "repo": repo,
                    "branch": branch,
                    "commits": [
                        {
                            "sha": c.get("sha", ""),
                            "message": (c.get("commit") or {}).get("message", ""),
                            "diff": self.get_commit_diff(repo, c.get("sha", "")),
                        }
                        for c in commits
                    ],
                })
                print(f"[monitor] {module} 检测到 {len(commits)} 个新提交，最新 {commits[0].get('sha', '')[:7]}")
            else:
                print(f"[monitor] {module} 无新提交")

        return changes, new_state

    def _force_lookback(self, repo: str, branch: str) -> List[Dict]:
        """时间窗内的提交（旧->新），用于无从比对水位时的兜底。"""
        lookback_hours = int(os.getenv("SYNC_LOOKBACK_HOURS", "24") or "24")
        since_dt = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
        return self._get_commits_since(repo, branch, since_dt.isoformat())

    @staticmethod
    def _truncate_at_watermark(commits: List[Dict], last_sha: str) -> List[Dict]:
        """兜底结果里如果碰巧含旧水位，砍掉它之前的内容，避免重复处理已同步的提交。"""
        for i, c in enumerate(commits):
            if c.get("sha") == last_sha:
                return commits[i + 1:]
        return commits

    def _get_commits_since(self, repo: str, branch: str, since_iso: str) -> List[Dict]:
        url = f"https://api.github.com/repos/{repo}/commits"
        params = {"sha": branch, "per_page": 100, "since": since_iso}
        try:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
            return resp.json() or []
        except Exception as e:
            print(f"[monitor] 获取 {repo} since-commits 失败: {e}")
            return []

    def save_state(self, state: Dict):
        self._save_state(state)


if __name__ == "__main__":
    monitor = GitHubMonitor()
    changes, new_state = monitor.check_for_updates(force_latest=True)
    print(f"共 {len(changes)} 个仓库有更新")
    for c in changes:
        print(f"  {c['module']}: {len(c['commits'])} commits")
