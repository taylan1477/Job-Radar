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

    # Çince deneyim yılı (Kullanıcı Kuralı: Asla 0 verilmez, deneyim yoksa 1)
    ans_years = gen.answer_form_question("How many years of work experience do you have with Chinese?")
    assert ans_years == "1"


def test_salary_expectation_questions():
    """Ücret / Maaş beklentisi soruları (Asla 'Evet' olmamalı, 35000 TL veya döviz olmalı)."""
    gen = ApplicationGenerator()
    assert gen.answer_form_question("Ücret beklentiniz nedir?") == "35000"
    assert gen.answer_form_question("Maaş beklentiniz nedir?") == "35000"
    assert gen.answer_form_question("Expected salary (monthly)") == "35000"
    assert gen.answer_form_question("Expected annual salary (USD)") == "25000"
    assert gen.answer_form_question("Hourly wage expectation") == "200"

    # Dropdown seçenekleri ile
    opts = ["Select an option", "20.000 TL - 30.000 TL", "30.000 TL - 40.000 TL", "40.000 TL - 50.000 TL"]
    assert gen.answer_form_question("Ücret beklentisi aralığı", opts) == "30.000 TL - 40.000 TL"


def test_user_specified_skills_years():
    """Kullanıcı Talebi: SQL: 3, .NET Core: 1, C#: 3, Asla 0 yıl tecrübe yok."""
    gen = ApplicationGenerator()
    assert gen.answer_form_question("SQL ile kaç yıllık iş deneyiminiz var?") == "3"
    assert gen.answer_form_question(".NET Core ile kaç yıllık iş deneyiminiz var?") == "1"
    assert gen.answer_form_question("C# ile kaç yıllık iş deneyiminiz var?") == "3"


def test_experience_years_rule_no_zero():
    """Kullanıcı Kuralı: 'Kaç yıl deneyiminiz var?' sorusuna asla '0' denmez. Varsa '3', Yoksa '1' denir."""
    gen = ApplicationGenerator()

    # 1. Deneyim olan alanlar -> "3"
    assert gen.answer_form_question("How many years of Unity experience do you have?") == "3"
    assert gen.answer_form_question("Kaç yıl C# tecrübeniz var?") == "3"
    assert gen.answer_form_question("Python deneyim yılı?") == "3"
    assert gen.answer_form_question("Kaç yıl yazılım geliştirme deneyiminiz var?") == "3"

    # 2. Deneyim olmayan alanlar -> "1" (asla "0" olmamalı)
    assert gen.answer_form_question("How many years of Java experience do you have?") == "1"
    assert gen.answer_form_question("Kaç yıl Flutter deneyiminiz var?") == "1"
    assert gen.answer_form_question("How many years of work experience do you have with Chinese?") == "1"
    assert gen.answer_form_question("Kaç yıl Ruby on Rails tecrübeniz var?") == "1"

    # 3. Seçenekli (dropdown) deneyim yılı sorularında eşleşme
    year_options = ["Select an option", "0", "1", "2", "3", "4+"]
    # Varsa -> "3"
    assert gen.answer_form_question("Years of experience with Unity", year_options) == "3"
    # Yoksa -> "1" (asla "0" seçilmez)
    assert gen.answer_form_question("Years of experience with Rust", year_options) == "1"


def test_answer_form_question_known_languages_and_skills():
    gen = ApplicationGenerator()

    # İngilizce
    opts_en = ["Select an option", "Native or bilingual", "Professional working", "Elementary", "None"]
    ans_en = gen.answer_form_question("English proficiency", opts_en)
    assert ans_en == "Professional working"

    # Unity / C# (Deneyim varsa 3)
    assert gen.answer_form_question("How many years of Unity experience do you have?") == "3"
    assert gen.answer_form_question("Kaç yıl C# tecrübeniz var?") == "3"

    # Vize sponsorluğu
    opts_spons = ["Yes", "No"]
    assert gen.answer_form_question("Will you now or in the future require visa sponsorship?", opts_spons) == "No"

    # Telefon Ülke Kodu (Asla Andorra (+376) seçmemeli, Turkey (+90) seçmeli)
    country_codes = [
        "Select an option",
        "Andorra (+376)",
        "United Arab Emirates (+971)",
        "Afghanistan (+93)",
        "Turkey (+90)",
        "United States (+1)"
    ]
    ans_code = gen.answer_form_question("Phone country code", country_codes)
    assert ans_code == "Turkey (+90)"
    assert ans_code != "Andorra (+376)"

