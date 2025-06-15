import subprocess


def count_commits(path):
    try:
        result = subprocess.run(
            ["git", "log", "--oneline"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.count("\n")
    except subprocess.CalledProcessError as e:
        if "does not have any commits yet" in e.stderr:
            return 0
        raise
