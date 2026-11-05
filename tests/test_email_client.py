from pathlib import Path
from src.clients.email_client import extract_emails, EmailClient


def test_extract_emails():
    sample_text = """
    Başvuru için lütfen ik@sirket.com veya kariyer@sirket.com.tr adresine CV'nizi iletiniz.
    Destek için support@example.com ile iletişime geçebilirsiniz.
    İletişim: info@oyunstüdyosu.com.
    """
    emails = extract_emails(sample_text)
    assert len(emails) >= 2
    # ik veya kariyer içerenler en başta olmalı
    assert any("ik@sirket.com" in e or "kariyer@sirket.com.tr" in e for e in emails[:2])
    # example.com elenmiş olmalı
    assert not any("example.com" in e for e in emails)


def test_email_client_dry_run(tmp_path):
    dummy_cv = tmp_path / "cv.pdf"
    dummy_cv.write_bytes(b"%PDF-1.4 dummy cv content")

    client = EmailClient(cv_path=dummy_cv)
    res = client.send_application(
        to_email="test@company.com",
        subject="İş Başvurusu: Game Developer",
        body="Merhaba, başvurum ektedir.",
        dry_run=True
    )
    assert res["success"] is True
    assert res["dry_run"] is True


def test_email_client_invalid_email():
    client = EmailClient()
    res = client.send_application(
        to_email="invalid-email-format",
        subject="Test",
        body="Test",
        dry_run=False
    )
    assert res["success"] is False
    assert "Geçersiz" in res["reason"]
