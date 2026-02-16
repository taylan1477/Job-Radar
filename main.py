# main.py – Job Radar: RSS + Skor + Google Sheets Pipeline

import argparse
from rss_sources import fetch_all_jobs
from scorer import score_job
from sheets_client import append_jobs, _get_sheet


def print_job_summary(job, index):
    """Tek bir ilanın özetini konsola yazdırır."""
    score = job.get("total_score", 0)

    # Skor rengini belirle
    if score >= 3.5:
        indicator = "🟢"
    elif score >= 2.0:
        indicator = "🟡"
    else:
        indicator = "🔴"

    print(f"  {indicator} [{score:.1f}] {job['title']}")
    print(f"      Firma: {job.get('company', '-') or '-'}")
    print(f"      Alan: {job.get('field', '-')} | Lokasyon: {job.get('location', '-')} | Level: {job.get('level', '-')}")
    print(f"      Kaynak: {job.get('source', '-')}")
    print(f"      Link: {job.get('link', '-')}")
    print()


def run(dry_run=False):
    """Ana pipeline: fetch → score → deduplicate → write."""
    print("=" * 60)
    print("  🎯 Job Radar v0.1 – RSS + Skor Pipeline")
    print("=" * 60)

    # 1. RSS'lerden ilanları çek
    jobs = fetch_all_jobs()

    if not jobs:
        print("❌ Hiç ilan bulunamadı. RSS kaynaklarını kontrol edin.")
        return

    # 2. Her ilanı skorla
    print("🧠 İlanlar skorlanıyor...\n")
    scored_jobs = [score_job(job) for job in jobs]

    # 3. Skora göre sırala (yüksekten düşüğe)
    scored_jobs.sort(key=lambda j: j.get("total_score", 0), reverse=True)

    # 4. Sonuçları göster
    print("=" * 60)
    print(f"  📋 Skorlanmış İlanlar (Toplam: {len(scored_jobs)})")
    print("=" * 60)
    print()

    # En iyi 20 ilanı göster
    display_count = min(20, len(scored_jobs))
    for i, job in enumerate(scored_jobs[:display_count]):
        print_job_summary(job, i + 1)

    if len(scored_jobs) > display_count:
        print(f"  ... ve {len(scored_jobs) - display_count} ilan daha.\n")

    # İstatistikler
    high_score = [j for j in scored_jobs if j.get("total_score", 0) >= 3.5]
    mid_score = [j for j in scored_jobs if 2.0 <= j.get("total_score", 0) < 3.5]
    low_score = [j for j in scored_jobs if j.get("total_score", 0) < 2.0]

    print("=" * 60)
    print(f"  📊 Özet")
    print(f"     🟢 Yüksek skor (≥3.5): {len(high_score)} ilan")
    print(f"     🟡 Orta skor (2.0-3.5): {len(mid_score)} ilan")
    print(f"     🔴 Düşük skor (<2.0):   {len(low_score)} ilan")
    print("=" * 60)

    # 5. Google Sheets'e yaz (dry_run değilse)
    if dry_run:
        print("\n⚠️  DRY RUN modu – Google Sheets'e yazılmadı.")
        print("   Gerçek çalıştırmak için: python main.py")
    else:
        print("\n📝 Google Sheets'e yazılıyor...\n")
        added, duplicates = append_jobs(scored_jobs)
        print(f"\n  ✅ Eklenen: {added} | ♻️ Duplicate: {duplicates}")

    print("\n🏁 Tamamlandı!\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Radar – RSS İlan Skor Pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Sheet'e yazmadan sadece konsola yazdır",
    )
    args = parser.parse_args()

    run(dry_run=args.dry_run)
