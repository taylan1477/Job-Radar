# test_lang.py
import sys
import io

# Windows konsol encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from scorer import score_job

samples = [
    {
        "title": "Desarrollador Java Senior",
        "summary": "Buscamos un desarrollador Java con experiencia en Spring Boot. Idioma: Español.",
        "location": "Madrid, Spain",
        "company": "Empresa ES"
    },
    {
        "title": "Softwareentwickler C#",
        "summary": "Wir suchen einen erfahrenen C# Entwickler. Standort: Berlin.",
        "location": "Berlin, Germany",
        "company": "Firma DE"
    },
    {
        "title": "Software Engineer (English)",
        "summary": "We move fast and break things. Join us in London.",
        "location": "London, UK",
        "company": "Startup UK"
    },
    {
        "title": "Yazılım Mühendisi",
        "summary": "Ankara ofisimiz için takım arkadaşı arıyoruz.",
        "location": "Ankara",
        "company": "Teknoloji A.Ş."
    }
]

print("--- Language Detection Test ---")
for job in samples:
    scored = score_job(job)
    print(f"\nTitle: {scored['title']}")
    print(f"Location: {scored['location']}")
    print(f"Total Score: {scored['total_score']}")
