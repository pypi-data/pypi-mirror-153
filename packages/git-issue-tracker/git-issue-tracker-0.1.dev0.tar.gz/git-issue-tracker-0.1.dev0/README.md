# Git issue tracker

This app track changes in git by receiving web hook from BitBucket and synchronize found issues
with Jira in terms of fix version. So it gives 100% guarantee that fix version is set correctly.

BitBucket or Jira could be changed to any other Git or Bug tracker system (should be written by your own). 


## How does it work

1. Webhook (on push) should be set up on the git server.
2. Git itself should be installed where this application is started
3. Extend `IssueHandler` and implement your own workflow with your bug-tracker system.
IE, set **fixVersion** directly to each task or only for story without subtasks or just add
comment where it was merged. For myself I used it together with [automationforjira] for 
further no-code processing of received data.
4. Extend `WebHookDataParser` if you use as git server something different from BitBucket. 

## Variables to override if needed 

- `TRACKED_BRANCH_REGEXP` : which branches do we track, by default it is set to 
`(release/.*|hotfix/.*|support/.*|develop|dev)`. Here is used git-flow branch model
- `MERGE_PATTERN_SEARCH_TO_SKIP` : merge pattern which should not be tracked, by default it is set to
`Merge.*((release\/|support\/|hotfix\/)|(tag)).*(develop|dev).*`.
- `WHITE_LISTED_REPOS` : repositories' name which available for further processing, by default 



[automationforjira]: https://automationforjira.com/