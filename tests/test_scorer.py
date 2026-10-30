import sys
import io

# Windows konsol encoding fix
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
        "title": "Senior Unity Developer",
        "summary": "We are looking for a game developer with 5+ years experience in Unity.",
        "location": "Remote in Ankara",
        "company": "Game Studio A"
    },
    {
        "title": "Simülasyon Mühendisi",
        "summary": "Askeri simülasyon ve sistem entegrasyonu projeleri. C4ISR ve HLA.",
        "location": "Ankara",
        "company": "Savunma Sanayii"
    },
    {
        "title": "Sistem Yöneticisi / NOC",
        "summary": "Linux sunucular ve veri merkezi altyapı yönetimi. Ağ operasyonları.",
        "location": "Ankara",
        "company": "Teknoloji A.Ş."
    },
    {
        "title": "ERP Uzmanı / Geliştiricisi",
        "summary": "SAP ve süreç otomasyonu, depo yönetim sistemleri.",
        "location": "İstanbul",
        "company": "Üretim Sanayi"
    },
    {
        "title": "Veritabanı Yöneticisi (DBA)",
        "summary": "SQL veritabanı yönetimi ve ETL iş zekası raporlama.",
        "location": "Remote",
        "company": "Finans Ltd"
    }
]

def test_scorer_all_samples():
    for job in samples:
        res = score_job(job)
        assert res["total_score"] > 0
        assert res["field"] in ["gamedev", "savunma_simülasyon", "sistem_network", "endüstriyel_otomasyon", "veri_bi", "yazılım", "diğer"]

if __name__ == "__main__":
    for s in samples:
        scored = score_job(s)
        print(f"[{scored['field']}] [{scored['total_score']}] {scored['title']}")
