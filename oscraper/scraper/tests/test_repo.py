import pytest

from oscraper.scraper.repo import ScraperRepo
from oscraper.scraper.tests.conftest import count_commits


@pytest.fixture
def repo(tmp_path):
    return ScraperRepo(tmp_path)


def test_commit_if_changed_initializes_repo_if_needed(repo, tmp_path):
    assert not (tmp_path / ".git").exists()
    assert not repo.commit_if_changed()
    assert (tmp_path / ".git").exists()


def test_commit_if_changed_returns_false_when_no_changes(repo, tmp_path):
    assert not repo.commit_if_changed()
    assert count_commits(tmp_path) == 0


def test_commit_if_changed_commits_new_file(repo, tmp_path):
    (tmp_path / "test.txt").write_text("test")
    assert repo.commit_if_changed()
    assert count_commits(tmp_path) == 1


def test_commit_if_changed_commits_modified_file(repo, tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test")
    repo.commit_if_changed()
    test_file.write_text("modified")
    assert repo.commit_if_changed()
    assert count_commits(tmp_path) == 2
