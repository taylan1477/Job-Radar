from pathlib import Path
from src.clients.easy_apply_client import LinkedInEasyApplyClient


def test_easy_apply_missing_session(tmp_path):
    fake_session = tmp_path / "non_existent_state.json"
    client = LinkedInEasyApplyClient(session_file=fake_session)

    assert client.has_valid_session() is False

    res = client.apply_to_job("https://www.linkedin.com/jobs/view/1234567890", dry_run=True)
    assert res["success"] is False
    assert "linkedin_state.json" in res["reason"]
