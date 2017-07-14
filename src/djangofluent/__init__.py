import raven.exceptions

try:
    version_sha = raven.fetch_git_sha('..')
except raven.exceptions.InvalidGitRepository:
    version_sha = None  # for unit testing
