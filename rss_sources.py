# rss_sources.py – RSS Feed Cekme Modulu v0.2

import feedparser
from datetime import datetime

# ──────────────────────────────────────────────
# RSS Kaynak Listesi – Sadece calisan feed'ler
# ──────────────────────────────────────────────

RSS_FEEDS = [
    {
        "name": "WeWorkRemotely",
        "url": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    },
    {
        "name": "Himalayas",
        "url": "https://himalayas.app/jobs/rss",
    },
]


def _parse_entry(entry, source_name):
    """Tek bir RSS entry'sini standart job dict'e cevirir."""
    title = entry.get("title", "").strip()
    link = entry.get("link", "").strip()
    summary = entry.get("summary", entry.get("description", "")).strip()

    # Firma adini bulmaya calis
    company = ""
    if hasattr(entry, "author"):
        company = entry.author
    elif " at " in title:
        parts = title.split(" at ", 1)
        company = parts[1].strip() if len(parts) > 1 else ""
    elif " - " in title:
        parts = title.rsplit(" - ", 1)
        company = parts[1].strip() if len(parts) > 1 else ""

    # Yayin tarihi
    published = ""
    if hasattr(entry, "published"):
        published = entry.published
    elif hasattr(entry, "updated"):
        published = entry.updated
    else:
        published = datetime.now().strftime("%Y-%m-%d")

    return {
        "title": title,
        "company": company,
        "link": link,
        "summary": summary,
        "published": published,
        "source": source_name,
    }


def fetch_feed(feed_info):
    """Tek bir RSS feed'i ceker ve job listesi dondurur."""
    name = feed_info["name"]
    url = feed_info["url"]
    jobs = []

    try:
        print(f"  [RSS] {name} cekiliyor... ", end="", flush=True)
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            print("[UYARI] Hata (atlaniyor)")
            return jobs

        for entry in feed.entries:
            job = _parse_entry(entry, name)
            if job["title"] and job["link"]:
                jobs.append(job)

        print(f"[OK] {len(jobs)} ilan bulundu")

    except Exception as e:
        print(f"[HATA] {e}")

    return jobs


def fetch_all_jobs():
    """Tum RSS kaynaklarindan ilanlari ceker."""
    all_jobs = []

    print("\n[INFO] RSS kaynaklari taraniyor...\n")

    for feed_info in RSS_FEEDS:
        jobs = fetch_feed(feed_info)
        all_jobs.extend(jobs)

    print(f"\n[INFO] RSS'ten toplam {len(all_jobs)} ilan cekildi.\n")
    return all_jobs
