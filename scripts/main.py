import os
import sys
from typing import List, Dict

from config import config
from monitor import GitHubMonitor
from doc_gen import DocGenerator


class MainController:
    def __init__(self):
        self.monitor = GitHubMonitor()
        self.doc_gen = DocGenerator()
        self.written_files: List[str] = []
        self.module_summaries: List[str] = []

    def run(self, force_latest: bool = False):
        print("=== CTNH-Docs 自动同步开始 ===")
        try:
            changes, new_state = self.monitor.check_for_updates(force_latest=force_latest)
            if not changes:
                print("🏁 未发现新变更。退出。")
                return

            for change in changes:
                module = change["module"]
                print(f"📝 处理模块 {module}...")
                if module == "__main__":
                    # 主仓库变更：通常只影响根 AGENTS.md 的路由表，跳过自动生成
                    print(f"ℹ️ 主仓库 {config.MAIN_REPO} 有 {len(change['commits'])} 个新提交；"
                          f"根 AGENTS.md 由人工维护，跳过 LLM 生成。")
                    self.module_summaries.append(
                        f"- 主仓库 {config.MAIN_REPO} 更新 {len(change['commits'])} 个提交（根路由表需人工核对）")
                    continue

                updates = self.doc_gen.generate_module_updates(change)
                if not updates:
                    print(f"ℹ️ {module} 无需更新或 LLM 未产出有效更新。")
                    continue
                written = self.doc_gen.apply_updates(updates)
                self.written_files.extend(written)
                self.module_summaries.append(
                    f"- **{module}**：更新 {len(written)} 个文档（{change['branch']} 分支 {len(change['commits'])} 个新提交）")

            # 全部成功后才推进 state
            self.monitor.save_state(new_state)
            print("💾 状态记录已更新。")
            self.output_summary()
        except Exception as e:
            print(f"💥 主循环错误: {e}")
            sys.exit(1)
        print("=== CTNH-Docs 自动同步完成 ===")

    def output_summary(self):
        if not self.written_files:
            print("📝 没有文件被更新。")
            return
        print(f"总计更新文件数: {len(self.written_files)}")
        for f in self.written_files:
            print(f"- {f}")

        if os.getenv("GITHUB_ACTIONS") == "true":
            github_output = os.getenv("GITHUB_OUTPUT")
            if github_output:
                pr_title = f"docs: 自动同步模块文档 ({len(self.written_files)} 个文件)"
                pr_body = "🤖 CTNH-Docs 自动同步。\n\n"
                pr_body += "### 模块更新\n" + "\n".join(self.module_summaries) + "\n\n"
                pr_body += "### 更新文件\n" + "\n".join(f"- {f}" for f in self.written_files) + "\n"
                with open(github_output, "a", encoding="utf-8") as f:
                    f.write("has_updates=true\n")
                    f.write(f"files_count={len(self.written_files)}\n")
                    f.write(f"pr_title={pr_title}\n")
                    f.write("pr_body<<EOF\n")
                    f.write(f"{pr_body}\nEOF\n")
            print("[GHA] has_updates=true")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CTNH-Docs 自动同步")
    parser.add_argument("--force-latest", action="store_true", help="强制同步最新提交")
    args = parser.parse_args()
    controller = MainController()
    controller.run(force_latest=args.force_latest)
