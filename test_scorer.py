# test_scorer.py
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
        "title": "Senior Unity Developer",
        "summary": "We are looking for a game developer with 5+ years experience in C# and Unity.",
        "location": "Remote in Ankara",
        "company": "Game Studio A"
    },
    {
        "title": "Backend Engineer",
        "summary": "Experience with Python, Django and AWS. 3 years minimum.",
        "location": "Istanbul",
        "company": "Tech Corp"
    },
    {
        "title": "Yazılım Geliştirici",
        "summary": "Genel başvuru. Java ve Spring Boot bilen.",
        "location": "Ankara (Hybrid)",
        "company": "Bank B"
    },
    {
        "title": "Frontend Developer",
        "summary": "React and TypeScript expert needed.",
        "location": "Berlin",
        "company": "Startup C"
    }
]

print("--- Scorer v0.5 Test ---")
for job in samples:
    scored = score_job(job)
    print(f"\nTitle: {scored['title']}")
    print(f"Field: {scored['field']} (Score: {scored.get('field_score', 'N/A')})")
    print(f"Location: {scored['location']} (Score: {scored.get('location_score', 'N/A')})")
    print(f"Level: {scored['level']} (Score: {scored.get('level_score', 'N/A')})")
    print(f"Total: {scored['total_score']}")
