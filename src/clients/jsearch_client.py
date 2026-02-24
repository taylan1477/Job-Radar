# jsearch_client.py – JSearch API (RapidAPI) Client

import requests
from src.utils.config import JSEARCH_API_KEY, JSEARCH_QUERIES

API_URL = "https://jsearch.p.rapidapi.com/search"


def _search_jobs(query, location="", remote_only=False, num_pages=1):
    """JSearch API'den ilan arar."""
    if not JSEARCH_API_KEY:
        return []

    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com",
    }

    params = {
        "query": query,
        "page": "1",
        "num_pages": str(num_pages),
    }

    if location:
        params["query"] = f"{query} in {location}"

    if remote_only:
        params["remote_jobs_only"] = "true"

    # 2 deneme, 30 saniye timeout
    for attempt in range(2):
        try:
            response = requests.get(API_URL, headers=headers, params=params, timeout=(10, 60))

            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            elif response.status_code == 429:
                print("[UYARI] JSearch API limit asildi (200/ay)")
                return []
            elif response.status_code == 403:
                print("[UYARI] JSearch API erisim engellendi – API key'i kontrol edin")
                return []
            else:
                print(f"[UYARI] JSearch API HTTP {response.status_code}")
                return []

        except requests.exceptions.Timeout:
            if attempt == 0:
                print("[TEKRAR] Timeout, yeniden deneniyor... ", end="", flush=True)
                continue
            print("[HATA] JSearch API: Timeout (2 deneme basarisiz)")
            return []
        except Exception as e:
            print(f"[HATA] JSearch API: {e}")
            return []

    return []


def _parse_jsearch_job(raw_job):
    """JSearch API sonucunu standart job dict'e cevirir."""
    title = raw_job.get("job_title", "").strip()
    company = raw_job.get("employer_name", "").strip()
    link = raw_job.get("job_apply_link", "") or raw_job.get("job_google_link", "")
    city = raw_job.get("job_city", "")
    state = raw_job.get("job_state", "")
    country = raw_job.get("job_country", "")
    is_remote = raw_job.get("job_is_remote", False)

    # Aciklama olustur
    location_parts = [p for p in [city, state, country] if p]
    location_str = ", ".join(location_parts)
    if is_remote:
        location_str = f"Remote - {location_str}" if location_str else "Remote"

    description = raw_job.get("job_description", "")[:500]  # Ilk 500 karakter

    summary = f"{location_str}. {description}"

    published = raw_job.get("job_posted_at_datetime_utc", "")
    if published:
        published = published[:10]  # YYYY-MM-DD

    return {
        "title": title,
        "company": company,
        "link": link.strip() if link else "",
        "summary": summary,
        "published": published,
        "source": "JSearch",
    }


def fetch_all_jsearch_jobs():
    """Tum JSearch aramalarini ceker."""
    if not JSEARCH_API_KEY:
        print("\n[INFO] JSearch API key tanimli degil – atlaniyor.")
        print("       Key almak icin: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch\n")
        return []

    all_jobs = []
    seen_links = set()

    print("\n[INFO] JSearch API (LinkedIn+Indeed+Glassdoor) taraniyor...\n")

    for search in JSEARCH_QUERIES:
        query = search["query"]
        location = search.get("location", "")
        remote_only = search.get("remote_only", False)

        label = f"'{query}'"
        if location:
            label += f" ({location})"
        if remote_only:
            label += " [Remote]"

        print(f"  [JSEARCH] {label} araniyor... ", end="", flush=True)

        results = _search_jobs(query, location, remote_only)

        count = 0
        for raw in results:
            job = _parse_jsearch_job(raw)
            if job["title"] and job["link"] and job["link"] not in seen_links:
                seen_links.add(job["link"])
                all_jobs.append(job)
                count += 1

        print(f"[OK] {count} ilan bulundu")

    print(f"\n[INFO] JSearch'ten toplam {len(all_jobs)} benzersiz ilan cekildi.\n")
    return all_jobs
