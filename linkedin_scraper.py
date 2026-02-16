# linkedin_scraper.py – LinkedIn Public Job Search Scraper (Playwright)

import time
import random
from datetime import datetime

from config import LINKEDIN_SEARCHES


def _build_search_url(keyword, location=""):
    """LinkedIn Jobs arama URL'si olusturur."""
    from urllib.parse import quote
    base = "https://www.linkedin.com/jobs/search/"
    params = [f"keywords={quote(keyword)}"]
    if location:
        params.append(f"location={quote(location)}")
    # Son 1 ay icindeki ilanlar
    params.append("f_TPR=r2592000")
    return f"{base}?{'&'.join(params)}"


def _parse_job_cards(page):
    """LinkedIn arama sonuc sayfasindan ilan kartlarini parse eder."""
    jobs = []
    seen = set()

    # Sayfa yuklenmesini bekle
    try:
        page.wait_for_selector("ul.jobs-search__results-list", timeout=10000)
    except Exception:
        # Alternatif selector dene
        try:
            page.wait_for_selector("div.job-search-card", timeout=5000)
        except Exception:
            print("[UYARI] LinkedIn ilan listesi bulunamadi")
            return jobs

    # Scroll ile daha fazla ilan yukle
    for _ in range(3):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(random.uniform(0.5, 1.0))

    # Ilan kartlarini bul
    cards = page.query_selector_all("div.base-card, div.job-search-card")

    for card in cards:
        try:
            # Baslik
            title_el = card.query_selector("h3.base-search-card__title, h3")
            title = title_el.inner_text().strip() if title_el else ""

            # Firma
            company_el = card.query_selector("h4.base-search-card__subtitle, a.hidden-nested-link")
            company = company_el.inner_text().strip() if company_el else ""

            # Lokasyon
            location_el = card.query_selector("span.job-search-card__location")
            location = location_el.inner_text().strip() if location_el else ""

            # Link
            link_el = card.query_selector("a.base-card__full-link, a[href*='/jobs/view/']")
            link = link_el.get_attribute("href") if link_el else ""

            if not title or not link:
                continue

            # Link temizle
            if "?" in link:
                link = link.split("?")[0]

            if link in seen:
                continue
            seen.add(link)

            # Tarih
            date_el = card.query_selector("time")
            published = ""
            if date_el:
                published = date_el.get_attribute("datetime") or ""
                if published:
                    published = published[:10]  # YYYY-MM-DD

            if not published:
                published = datetime.now().strftime("%Y-%m-%d")

            jobs.append({
                "title": title,
                "company": company,
                "link": link,
                "summary": location,
                "published": published,
                "source": "LinkedIn",
            })

        except Exception:
            continue

    return jobs


def fetch_linkedin_search(browser, search_config):
    """Tek bir LinkedIn aramasini ceker."""
    keyword = search_config["keyword"]
    location = search_config.get("location", "")
    location_label = location if location else "Global"

    url = _build_search_url(keyword, location)

    print(f"  [LINKEDIN] '{keyword}' ({location_label}) araniyor... ", end="", flush=True)

    try:
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()

        page.goto(url, timeout=30000)
        time.sleep(random.uniform(2, 4))  # Anti-bot: rastgele bekleme

        jobs = _parse_job_cards(page)
        print(f"[OK] {len(jobs)} ilan")

        context.close()
        return jobs

    except Exception as e:
        print(f"[HATA] {e}")
        try:
            context.close()
        except Exception:
            pass
        return []


def fetch_all_linkedin_jobs():
    """Tum LinkedIn aramalarini ceker."""
    if not LINKEDIN_SEARCHES:
        print("\n[INFO] LinkedIn aramalari tanimli degil – atlaniyor.\n")
        return []

    all_jobs = []
    seen_links = set()

    print("\n[INFO] LinkedIn Jobs taraniyor (Playwright)...\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[UYARI] Playwright yuklu degil. 'pip install playwright' calistirin.")
        return []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            for i, search in enumerate(LINKEDIN_SEARCHES):
                jobs = fetch_linkedin_search(browser, search)

                for job in jobs:
                    if job["link"] not in seen_links:
                        seen_links.add(job["link"])
                        all_jobs.append(job)

                # Aramalar arasi bekleme (anti-bot)
                if i < len(LINKEDIN_SEARCHES) - 1:
                    delay = random.uniform(3, 6)
                    time.sleep(delay)

            browser.close()

    except Exception as e:
        print(f"[HATA] Playwright browser hatasi: {e}")

    print(f"\n[INFO] LinkedIn'den toplam {len(all_jobs)} benzersiz ilan cekildi.\n")
    return all_jobs
