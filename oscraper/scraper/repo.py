import subprocess
from pathlib import Path


class ScraperRepo:
    def __init__(self, path: Path):
        self.path = path

    def init(self):
        subprocess.run(["git", "init"], cwd=self.path, check=True)
        subprocess.run(
            ["git", "config", "user.email", "scraper@example.com"],
            cwd=self.path,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Scraper Bot"],
            cwd=self.path,
            check=True,
        )

    def commit_if_changed(self) -> bool:
        if not (self.path / ".git").exists():
            self.init()

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=self.path,
            capture_output=True,
            text=True,
            check=True,
        )
        if not result.stdout:
            return False

        subprocess.run(["git", "add", "."], cwd=self.path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Update scraped data"],
            cwd=self.path,
            check=True,
        )
        return True
