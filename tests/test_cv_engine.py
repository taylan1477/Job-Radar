import os
from pathlib import Path
import pytest

from src.core.cv_engine import CVEngine, MASTER_PROJECTS, KNOWN_SKILLS


@pytest.fixture
def cv_engine(tmp_path):
    output_dir = tmp_path / "generated"
    return CVEngine(output_dir=output_dir)


def test_hybrid_routing_high_score(cv_engine, monkeypatch):
    """Skor >= 4.0 olan VIP ilanların otomatik olarak Mod 2 (Sıcak JIT) seçtiğini doğrular."""
    # Mock generate_tailored_cv so we don't compile PDF in pure routing test
    monkeypatch.setattr(cv_engine, "generate_tailored_cv", lambda job: Path("mock_tailored.pdf"))

    job = {
        "title": "Senior Game Developer",
        "company": "Dream Games",
        "score": 4.5,
        "link": "https://www.linkedin.com/jobs/view/12345",
        "field": "Game"
    }

    path, mode, reason = cv_engine.resolve_cv_for_job(job)
    assert mode == "Mod 2 (İlana Özel Sıcak CV)"
    assert "VIP İlan" in reason
    assert path.name == "mock_tailored.pdf"


def test_hybrid_routing_external_job(cv_engine, monkeypatch):
    """LinkedIn dışı (Easy Apply olmayan) ilanların otomatik olarak Mod 2 seçtiğini doğrular."""
    monkeypatch.setattr(cv_engine, "generate_tailored_cv", lambda job: Path("mock_tailored.pdf"))

    job = {
        "title": "Backend Developer",
        "company": "KariyerNet Co",
        "score": 3.2,
        "link": "https://www.kariyer.net/is-ilani/12345",
        "field": "Software"
    }

    path, mode, reason = cv_engine.resolve_cv_for_job(job)
    assert mode == "Mod 2 (İlana Özel Sıcak CV)"
    assert "Harici İlan" in reason
    assert path.name == "mock_tailored.pdf"


def test_hybrid_routing_standard_easy_apply(cv_engine, monkeypatch):
    """Skor < 4.0 ve Easy Apply olan ilanların hızlı Mod 1 (Katalog) seçtiğini doğrular."""
    monkeypatch.setattr(cv_engine, "match_catalog_cv", lambda job: Path("mock_catalog.pdf"))

    job = {
        "title": "Junior Python Developer",
        "company": "Tech Corp",
        "score": 3.5,
        "link": "https://www.linkedin.com/jobs/view/99999",
        "field": "Automation"
    }

    path, mode, reason = cv_engine.resolve_cv_for_job(job)
    assert mode == "Mod 1 (Katalog Eşleme)"
    assert "Standart LinkedIn Easy Apply" in reason
    assert path.name == "mock_catalog.pdf"


def test_forced_modes(cv_engine, monkeypatch):
    """Zorunlu force_mode parametresinin doğru çalıştığını doğrular."""
    monkeypatch.setattr(cv_engine, "match_catalog_cv", lambda job: Path("catalog.pdf"))
    monkeypatch.setattr(cv_engine, "generate_tailored_cv", lambda job: Path("tailored.pdf"))

    job = {"title": "Developer", "score": 4.8, "link": "https://www.kariyer.net/1"}
    
    # Normalde Mod 2 olmalı ama force_mode=catalog ile Mod 1 olmalı
    p1, m1, _ = cv_engine.resolve_cv_for_job(job, force_mode="catalog")
    assert m1 == "Mod 1 (Katalog Eşleme)"
    assert p1.name == "catalog.pdf"

    job_low = {"title": "Developer", "score": 2.5, "link": "https://www.linkedin.com/1"}
    # Normalde Mod 1 olmalı ama force_mode=tailored ile Mod 2 olmalı
    p2, m2, _ = cv_engine.resolve_cv_for_job(job_low, force_mode="tailored")
    assert m2 == "Mod 2 (İlana Özel Sıcak CV)"
    assert p2.name == "tailored.pdf"


def test_catalog_matching(cv_engine):
    """Katalog eşleştirmesinin oyun, yapay zeka ve genel yazılım için doğru PDF'i seçtiğini doğrular."""
    # 1. Game
    game_job = {"title": "Unity Game Developer", "field": "GameDev", "description": "Physics and 3D gameplay"}
    game_cv = cv_engine.match_catalog_cv(game_job)
    assert "Game_Simulation" in game_cv.name

    # 2. Automation / AI
    ai_job = {"title": "AI & Automation Engineer", "field": "AI", "description": "Web scraping, computer vision and PyTorch"}
    ai_cv = cv_engine.match_catalog_cv(ai_job)
    assert "Automation_AI" in ai_cv.name

    # 3. Backend / Software
    backend_job = {"title": "Java Spring Boot Developer", "field": "Software", "description": "PostgreSQL and REST APIs"}
    backend_cv = cv_engine.match_catalog_cv(backend_job)
    assert "Software_Systems" in backend_cv.name


def test_skill_positioning_rules(cv_engine):
    """
    Kullanıcı Yetkinlik Konumlandırma Kuralını Doğrular:
    - Bilinen yetkinlikler -> Proficient / Advanced
    - İlandaki bilinmeyen yetkinlikler -> Intermediate / Working Knowledge
    """
    job_text = "we are looking for a go, kotlin developer with strong c#, python and docker knowledge using aws and redis"
    proficient, intermediate = cv_engine._position_skills_for_job(job_text)

    # C#, Python, Docker bildiğimiz yetkinlikler (Proficient)
    assert any("C#" in s for s in proficient)
    assert any("Python" in s for s in proficient)
    assert any("Docker" in s for s in proficient)

    # Go, Kotlin, AWS, Redis bilmediğimiz ancak ilanda istenen yetkinlikler (Intermediate)
    assert any("GO" in s.upper() for s in intermediate)
    assert any("KOTLIN" in s.upper() for s in intermediate)
    assert any("AWS" in s.upper() for s in intermediate)
    assert any("REDIS" in s.upper() for s in intermediate)


def test_top_projects_selection(cv_engine):
    """11 Proje arasından ilanın alanına göre en uygun 3 projenin seçildiğini doğrular."""
    # Unity / Game
    game_projects = cv_engine._select_top_projects("unity c# multiplayer combat burst job system", "gamedev")
    assert len(game_projects) == 3
    ids = [p["id"] for p in game_projects]
    assert "aegis_forge" in ids or "evolucat" in ids or "soloidle" in ids

    # Java / Backend
    backend_projects = cv_engine._select_top_projects("java spring boot postgresql ffmpeg desktop", "software")
    assert len(backend_projects) == 3
    assert any(p["id"] == "mass_video_cutter" for p in backend_projects)


def test_pdf_compilation(cv_engine, tmp_path):
    """Playwright Headless ile gerçek A4 PDF derleme testini doğrular."""
    job = {
        "title": "Fullstack Software Engineer",
        "company": "Test Company",
        "field": "Software",
        "description": "Looking for React Native, TypeScript and PostgreSQL developer",
        "score": 4.2,
        "link": "https://www.linkedin.com/jobs/view/123"
    }

    pdf_path = cv_engine.generate_tailored_cv(job)
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 5000  # Geçerli ve içerikli bir PDF olmalı
