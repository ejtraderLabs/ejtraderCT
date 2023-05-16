from github import Github
import setuptools
import re

# Leitura da versão do setup.py
setup_args = {}
exec(open("setup.py", "r").read(), setup_args)
setup_version = setup_args["version"]

# Acessa o repositório atual
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))

# Busca a última release
releases = repo.get_releases()
latest_release = next(releases.get_page(0))

# Se a versão do setup.py for diferente da última release, cria uma nova release
if latest_release.tag_name != setup_version:
    repo.create_git_ref(ref=f"refs/tags/{setup_version}", sha=os.getenv("GITHUB_SHA"))
    repo.create_git_release(
        tag=setup_version,
        name=f"Release {setup_version}",
        message="",
        draft=False,
        prerelease=False,
    )
