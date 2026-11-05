from src.core.email_classifier import EmailClassifier


def test_classify_rejection_english():
    classifier = EmailClassifier()
    email_data = {
        "from": "Acme Talent Team <jobs@acme.com>",
        "subject": "Update on your application at Acme",
        "body": "Thank you for applying. Unfortunately, after careful consideration, we have decided to pursue other candidates who more closely align with our needs."
    }
    result = classifier.classify_email(email_data)
    assert result["status"] == "Reddedildi"
    assert result["confidence"] >= 0.9


def test_classify_rejection_turkish():
    classifier = EmailClassifier()
    email_data = {
        "from": "İK Departmanı <ik@sirket.com.tr>",
        "subject": "Başvurunuz Hakkında Bilgilendirme",
        "body": "Değerli Adayımız, başvurunuz incelenmiş olup bu pozisyon için başka adaylarla devam etme kararı aldığımızı üzülerek bildiririz."
    }
    result = classifier.classify_email(email_data)
    assert result["status"] == "Reddedildi"


def test_classify_interview_english():
    classifier = EmailClassifier()
    email_data = {
        "from": "Recruiter <recruiting@gamecorp.io>",
        "subject": "Invitation to Interview: Game Developer",
        "body": "We were very impressed with your background! We would like to schedule an interview with our engineering lead next week."
    }
    result = classifier.classify_email(email_data)
    assert result["status"] == "Mülakat"
    assert result["confidence"] >= 0.9


def test_classify_interview_turkish():
    classifier = EmailClassifier()
    email_data = {
        "from": "İnsan Kaynakları <ik@teknoloji.com.tr>",
        "subject": "Teknik Mülakat Daveti",
        "body": "Merhaba, başvurunuz olumlu değerlendirilmiştir. Bir sonraki aşama olarak online teknik mülakat planlamak istiyoruz."
    }
    result = classifier.classify_email(email_data)
    assert result["status"] == "Mülakat"


def test_classify_irrelevant():
    classifier = EmailClassifier()
    email_data = {
        "from": "Bülten Servisi <newsletter@weeklydev.io>",
        "subject": "This Week in Tech: New Python 3.14 Features",
        "body": "Discover the latest changes in Python, AI frameworks, and game development news."
    }
    result = classifier.classify_email(email_data)
    assert result["status"] == "İlgisiz"
