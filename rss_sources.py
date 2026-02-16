# rss_sources.py – RSS Feed Çekme Modülü

import feedparser
from datetime import datetime

# ──────────────────────────────────────────────
# RSS Kaynak Listesi
# Her kaynak: (isim, url, entry_parser fonksiyonu)
# ──────────────────────────────────────────────

RSS_FEEDS = [
    {
        "name": "WeWorkRemotely",
        "url": "https://weworkremotely.com/categories/remote-programming-jobs.rss",
    },
    {
        "name": "Remotive",
        "url": "https://remotive.com/remote-jobs/software-dev/feed",
    },
    {
        "name": "Hitmarker",
        "url": "https://hitmarker.net/feed/jobs",
    },
    {
        "name": "Himalayas",
        "url": "https://himalayas.app/jobs/rss",
    },
    {
        "name": "Jobicy",
        "url": "https://jobicy.com/feed/newjob",
    },
]


def _parse_entry(entry, source_name):
    """Tek bir RSS entry'sini standart job dict'e çevirir."""
    title = entry.get("title", "").strip()
    link = entry.get("link", "").strip()
    summary = entry.get("summary", entry.get("description", "")).strip()

    # Firma adını bulmaya çalış
    company = ""
    if hasattr(entry, "author"):
        company = entry.author
    elif " at " in title:
        # "Software Engineer at Google" formatı
        parts = title.split(" at ", 1)
        company = parts[1].strip() if len(parts) > 1 else ""
    elif " - " in title:
        # "Software Engineer - Google" formatı
        parts = title.rsplit(" - ", 1)
        company = parts[1].strip() if len(parts) > 1 else ""

    # Yayın tarihi
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
    """Tek bir RSS feed'i çeker ve job listesi döndürür."""
    name = feed_info["name"]
    url = feed_info["url"]
    jobs = []

    try:
        print(f"  📡 {name} çekiliyor... ", end="")
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            print(f"⚠️  Hata (atlanıyor)")
            return jobs

        for entry in feed.entries:
            job = _parse_entry(entry, name)
            if job["title"] and job["link"]:
                jobs.append(job)

        print(f"✅ {len(jobs)} ilan bulundu")

    except Exception as e:
        print(f"❌ Hata: {e}")

    return jobs


def fetch_all_jobs():
    """Tüm RSS kaynaklarından ilanları çeker."""
    all_jobs = []

    print("\n🔄 RSS kaynakları taranıyor...\n")

    for feed_info in RSS_FEEDS:
        jobs = fetch_feed(feed_info)
        all_jobs.extend(jobs)

    print(f"\n📊 Toplam {len(all_jobs)} ilan çekildi.\n")
    return all_jobs
