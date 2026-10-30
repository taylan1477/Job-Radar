import sys
import io

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from src.core.scorer import score_job

samples = [
    {
        "title": "Desarrollador Java Senior",
        "summary": "Buscamos un desarrollador con experiencia en Spring Boot. Idioma: Español.",
        "location": "Madrid, Spain",
        "company": "Empresa ES"
    },
    {
        "title": "Softwareentwickler",
        "summary": "Wir suchen einen erfahrenen Entwickler. Standort: Berlin.",
        "location": "Berlin, Germany",
        "company": "Firma DE"
    },
    {
        "title": "Frontend Developer",
        "summary": "We are looking for a frontend developer proficient in React and TypeScript.",
        "location": "Remote",
        "company": "US Corp"
    },
    {
        "title": "Kıdemli Oyun Geliştirici",
        "summary": "Mobil oyun projelerimizde çalışacak deneyimli geliştirici aranıyor.",
        "location": "Ankara",
        "company": "Oyun Stüdyosu TR"
    }
]

def test_language_detection():
    # Spanish -> Restricted
    s_es = score_job(samples[0])
    assert s_es["restricted"] is True
    assert s_es["location"] == "dead"
    
    # German -> Restricted
    s_de = score_job(samples[1])
    assert s_de["restricted"] is True
    assert s_de["location"] == "dead"
    
    # English -> Not restricted by language
    s_en = score_job(samples[2])
    assert s_en["restricted"] is False
    
    # Turkish -> Not restricted by language
    s_tr = score_job(samples[3])
    assert s_tr["restricted"] is False

if __name__ == "__main__":
    test_language_detection()
    print("Language tests passed!")
