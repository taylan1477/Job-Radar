from pathlib import Path
from src.clients.easy_apply_client import LinkedInEasyApplyClient
from src.core.application_generator import ApplicationGenerator


def test_easy_apply_missing_session(tmp_path):
    fake_session = tmp_path / "non_existent_state.json"
    client = LinkedInEasyApplyClient(session_file=fake_session)

    assert client.has_valid_session() is False

    res = client.apply_to_job("https://www.linkedin.com/jobs/view/1234567890", dry_run=True)
    assert res["success"] is False
    assert "linkedin_state.json" in res["reason"]


def test_answer_form_question_chinese_language():
    gen = ApplicationGenerator()
    
    # 1. Çince dil yeterlilik dropdown sorusu
    opts = ["Select an option", "Native or bilingual", "Full professional", "Professional working", "Limited working", "Elementary", "None"]
    ans = gen.answer_form_question("What is your proficiency level in Chinese?", opts)
    assert ans == "None"

    # Türkçe seçenekli Çince sorusu
    opts_tr = ["Lütfen seçiniz", "Anadili", "İleri Seviye", "Orta Seviye", "Temel", "Yok"]
    ans_tr = gen.answer_form_question("Çince dil bilginiz nedir?", opts_tr)
    assert ans_tr == "Yok"

    # Çince deneyim yılı (sayısal)
    ans_years = gen.answer_form_question("How many years of work experience do you have with Chinese?")
    assert ans_years == "0"


def test_answer_form_question_known_languages_and_skills():
    gen = ApplicationGenerator()

    # İngilizce
    opts_en = ["Select an option", "Native or bilingual", "Professional working", "Elementary", "None"]
    ans_en = gen.answer_form_question("English proficiency", opts_en)
    assert ans_en == "Professional working"

    # Unity / C#
    assert gen.answer_form_question("How many years of Unity experience do you have?") == "2"
    assert gen.answer_form_question("Kaç yıl C# tecrübeniz var?") == "3"

    # Vize sponsorluğu
    opts_spons = ["Yes", "No"]
    assert gen.answer_form_question("Will you now or in the future require visa sponsorship?", opts_spons) == "No"

