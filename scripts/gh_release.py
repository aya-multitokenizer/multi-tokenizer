"""GH Release script."""

from github_release import gh_release_create

import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

version = data["tool"]["poetry"]["version"]

gh_release_create(
    "chandralegend/multi-tokenizer",
    version,
    publish=True,
    name=f"v{version}",
    asset_pattern="dist/*",
    body="Release notes for MTLLM",
)
