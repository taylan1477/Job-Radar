# main.py – Job Radar v0.6.5: Interaktif Cok Kaynakli Skor Pipeline

import sys
import io
from src.clients.rss_sources import fetch_all_jobs as fetch_rss_jobs
from src.clients.kariyer_scraper import fetch_all_kariyer_jobs
from src.clients.jsearch_client import fetch_all_jsearch_jobs
from src.clients.linkedin_scraper import fetch_all_linkedin_jobs
from src.core.scorer import score_job
from src.clients.sheets_client import append_jobs, clear_sheet, fix_sheet

# Windows konsol encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions (<3.7)
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")


def print_job_summary(job):
    """Tek bir ilanin ozetini konsola yazdirir."""
    score = job.get("total_score", 0)
    restricted = job.get("restricted", False)

    if restricted:
        indicator = "[XXX]"
    elif score >= 3.5:
        indicator = "[+++]"
    elif score >= 2.0:
        indicator = "[++ ]"
    else:
        indicator = "[+  ]"

    print(f"  {indicator} [{score:.1f}] {job['title']}")
    print(f"      Firma: {job.get('company', '-') or '-'}")
    print(f"      Alan: {job.get('field', '-')} | Lokasyon: {job.get('location', '-')} | Level: {job.get('level', '-')}")
    print(f"      Kaynak: {job.get('source', '-')}")
    if restricted:
        print(f"      ** KISITLI (ulke/vize) - Atlanacak **")
    print()


def show_menu():
    """Interaktif menu gosterir ve secimi dondurur."""
    print()
    print("=" * 50)
    print("  Job Radar v0.3 - Interaktif Menu")
    print("=" * 50)
    print()
    print("  1. Tam calistir (tum kaynaklar)")
    print("  2. Temiz calistir (SIL + tum kaynaklar)")
    print("  3. API'siz calistir (LinkedIn + RSS, JSearch yok)")
    print("  4. Sadece API (JSearch)")
    print("  5. Dry Run (konsola yazdir, Sheet'e yazma)")
    print("  6. Tabloyu Duzelt (baslik/sutun/tarih/skor)")
    print("  7. Cikis")
    print()

    while True:
        choice = input("  Seciminiz (1-7): ").strip()
        if choice in ("1", "2", "3", "4", "5", "6", "7"):
            return choice
        print("  Gecersiz secim, tekrar deneyin.")


def run(dry_run=False, clear=False, sources=None):
    """
    Ana pipeline: fetch -> score -> filter -> deduplicate -> write.
    sources: hangi kaynaklarin kullanilacagi.
             None = hepsi, veya {"linkedin", "kariyer", "jsearch", "rss"} alt kumesi.
    """
    if sources is None:
        sources = {"linkedin", "kariyer", "jsearch", "rss"}

    print()
    print("=" * 60)
    print("  Job Radar v0.3 - Cok Kaynakli Skor Pipeline")
    print(f"  Kaynaklar: {', '.join(sorted(sources))}")
    print("=" * 60)

    # -- 0. Sheet temizleme (istege bagli) --
    if clear and not dry_run:
        print("\n[INFO] Eski veriler temizleniyor...\n")
        clear_sheet()

    # -- 1. Secilen kaynaklardan ilanlari cek --
    all_jobs = []

    if "linkedin" in sources:
        linkedin_jobs = fetch_all_linkedin_jobs()
        all_jobs.extend(linkedin_jobs)

    if "kariyer" in sources:
        kariyer_jobs = fetch_all_kariyer_jobs()
        all_jobs.extend(kariyer_jobs)

    if "jsearch" in sources:
        jsearch_jobs = fetch_all_jsearch_jobs()
        all_jobs.extend(jsearch_jobs)

    if "rss" in sources:
        rss_jobs = fetch_rss_jobs()
        all_jobs.extend(rss_jobs)

    if not all_jobs:
        print("[HATA] Hic ilan bulunamadi.")
        return

    # -- 2. Her ilani skorla --
    print("=" * 60)
    print("[INFO] Ilanlar skorlaniyor...\n")
    scored_jobs = [score_job(job) for job in all_jobs]

    # -- 3. Kisitli ilanlari ayir --
    restricted_jobs = [j for j in scored_jobs if j.get("restricted", False)]
    valid_jobs = [j for j in scored_jobs if not j.get("restricted", False)]

    # -- 4. Skora gore sirala --
    valid_jobs.sort(key=lambda j: j.get("total_score", 0), reverse=True)

    # -- 5. Sonuclari goster --
    print("=" * 60)
    print(f"  Skorlanmis Ilanlar (Gecerli: {len(valid_jobs)} | Kisitli: {len(restricted_jobs)})")
    print("=" * 60)
    print()

    # En iyi 25 ilani goster
    display_count = min(25, len(valid_jobs))
    for job in valid_jobs[:display_count]:
        print_job_summary(job)

    if len(valid_jobs) > display_count:
        print(f"  ... ve {len(valid_jobs) - display_count} ilan daha.\n")

    # -- 6. Istatistikler --
    high_score = [j for j in valid_jobs if j.get("total_score", 0) >= 3.5]
    mid_score = [j for j in valid_jobs if 2.0 <= j.get("total_score", 0) < 3.5]
    low_score = [j for j in valid_jobs if j.get("total_score", 0) < 2.0]

    source_counts = {}
    for j in valid_jobs:
        src = j.get("source", "?")
        source_counts[src] = source_counts.get(src, 0) + 1

    print("=" * 60)
    print("  OZET")
    print(f"     [+++] Yuksek skor (>=3.5): {len(high_score)} ilan")
    print(f"     [++ ] Orta skor (2.0-3.5): {len(mid_score)} ilan")
    print(f"     [+  ] Dusuk skor (<2.0):   {len(low_score)} ilan")
    print(f"     [XXX] Kisitli (atlanan):   {len(restricted_jobs)} ilan")
    print()
    print("  KAYNAK BAZLI:")
    for src, count in sorted(source_counts.items(), key=lambda x: -x[1]):
        print(f"     {src}: {count} ilan")
    print("=" * 60)

    # -- 7. Google Sheets'e yaz --
    if dry_run:
        print("\n[!] DRY RUN modu - Google Sheets'e yazilmadi.")
    else:
        print("\n[INFO] Google Sheets'e yaziliyor...\n")
        added, duplicates = append_jobs(valid_jobs)
        print(f"\n  [OK] Eklenen: {added} | [DUP] Duplicate: {duplicates}")
        
        # -- 8. Otomatik Tablo Duzeltme --
        print("\n[INFO] Tablo otomatik duzeltiliyor (Format/Smart Chips)...\n")
        fix_sheet()

    print("\n[BITTI] Tamamlandi!\n")


if __name__ == "__main__":
    choice = show_menu()

    if choice == "1":
        run(dry_run=False, clear=False)
    elif choice == "2":
        run(dry_run=False, clear=True)
    elif choice == "3": 
        run(dry_run=False, sources={"linkedin", "kariyer", "rss"})
    elif choice == "4":
        run(dry_run=False, sources={"jsearch"})
    elif choice == "5":
        run(dry_run=True, clear=False)
    elif choice == "6":
        print("\n[INFO] Tablo duzeltiliyor...\n")
        fix_sheet()
        print("\n[BITTI] Tamamlandi!\n")
    elif choice == "7":
        print("\nCikis yapiliyor...\n")
