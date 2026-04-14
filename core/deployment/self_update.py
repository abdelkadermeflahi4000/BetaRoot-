# core/deployment/self_update.py

import subprocess
import time

class SelfUpdater:

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def check_updates(self):
        subprocess.run(["git", "pull"], cwd=self.repo_path)

    def auto_update_loop(self):
        while True:
            print("[UPDATE] checking...")
            self.check_updates()
            time.sleep(60)
