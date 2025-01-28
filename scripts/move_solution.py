import re
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PYTHON_DIR = ROOT_DIR / 'kattis' / 'python'
README_FILE = ROOT_DIR / 'README.md'

def get_difficulty_label(folder_name: str) -> str:
    match = re.match(r'^\d+_(.*)', folder_name)
    return match.group(1) if match else folder_name

def update_readme():
    if not PYTHON_DIR.exists():
        raise FileNotFoundError(f"[Error] Directory does not exist: {PYTHON_DIR}")

    with open(README_FILE, 'w') as f:
        f.write("# Kattis Solutions\n\n")
        f.write("This repository shares solutions to Kattis problems in Python.\n\n")
        f.write("## Problems\n")
        f.write("| Problem | Difficulty | Language | Solution |\n")
        f.write("| ------- | ---------- | -------- | -------- |\n")

        for diff_dir in sorted(PYTHON_DIR.iterdir()):
            if diff_dir.is_dir():
                diff_name = get_difficulty_label(diff_dir.name)
                for py_file in sorted(diff_dir.glob("*.py")):
                    problem_name = py_file.stem
                    problem_url = f"https://open.kattis.com/problems/{problem_name.lower()}"
                    github_url = (
                        f"https://github.com/ImPlotting/kattisol/blob/main/"
                        f"kattis/python/{diff_dir.name}/{py_file.name}"
                    )
                    f.write(
                        f"| [{problem_name}]({problem_url}) "
                        f"| {diff_name} "
                        f"| Python "
                        f"| [Solution]({github_url}) |\n"
                    )

def git_operations():
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Auto update of solutions"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

def main():
    update_readme()
    git_operations()

if __name__ == "__main__":
    main()
