import os


GIT_USER_PASS = {
    "username": os.environ["GIT_USERNAME"],
    "token": os.environ["GIT_TOKEN"]
}

# Git properties
TRACKED_BRANCH_REGEXP = os.getenv("TRACKED_BRANCH_REGEXP", "(release/.*|hotfix/.*|support/.*|develop|dev)")
MERGE_PATTERN_SEARCH_TO_SKIP = os.getenv("MERGE_PATTERN_SEARCH_TO_SKIP", "Merge.*\b((release\/|support\/|hotfix\/)|(tag))\b.*\b(develop|dev)\b.*")
WHITE_LISTED_REPOS = os.getenv("WHITE_LISTED_REPOS", ".*")

# Issue tracker properties
ISSUE_TRACKER_PATTERN = os.getenv("ISSUE_TRACKER_PATTERN", ".*")




