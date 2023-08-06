from injector import singleton

from tracker.core.connectors.git.github import GithubHookParser
from tracker.core.connectors.issue_handler import IssueHandler, DummyIssueHandler
from tracker.core.connectors.webhook_parser import WebHookDataParser


def configure(binder):
    binder.bind(WebHookDataParser, to=GithubHookParser, scope=singleton)
    binder.bind(IssueHandler, to=DummyIssueHandler, scope=singleton)

