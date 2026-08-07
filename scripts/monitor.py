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

            if force_latest or not last_sha:
                # 强制或首次：只取最近 LOOKBACK 内的提交，避免历史洪流
                lookback_hours = int(os.getenv("SYNC_LOOKBACK_HOURS", "24") or "24")
                since_dt = datetime.now(timezone.utc) - timedelta(hours=lookback_hours)
                commits = self._get_commits_since(repo, branch, since_dt.isoformat())
            else:
                commits = self.get_latest_commits_since(repo, branch, since_sha=last_sha)

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
