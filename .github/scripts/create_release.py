from github import Github
import os
import re

# Leitura da versão do setup.py
with open("../../setup.py", "r") as f:
    setup_contents = f.read()

match = re.search(r"version\s*=\s*\'([^\']+)\',", setup_contents)
if match:
    setup_version = match.group(1)
else:
    raise ValueError("Could not find version in setup.py")

# Acessa o repositório atual
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))

# Busca a última release
releases = repo.get_releases()
latest_release = next((release for release in releases), None)

# Se a versão do setup.py for diferente da última release, cria uma nova release
if latest_release is None or latest_release.tag_name != setup_version:
    repo.create_git_ref(ref=f"refs/tags/{setup_version}", sha=os.getenv("GITHUB_SHA"))
    repo.create_git_release(
        tag=setup_version,
        name=f"Release {setup_version}",
        message="",
        draft=False,
        prerelease=False,
    )
