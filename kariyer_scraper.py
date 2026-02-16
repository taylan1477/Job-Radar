# kariyer_scraper.py – Kariyer.net Scraper v0.4 (Playwright)

import time
import re
import random
from datetime import datetime
from urllib.parse import quote

from config import KARIYER_SEARCHES, RELEVANCE_KEYWORDS

BASE_URL = "https://www.kariyer.net"
SEARCH_URL = "https://www.kariyer.net/is-ilanlari"

# Kariyer.net sehir kodlari
CITY_CODES = {
    "ankara": "006",
    "istanbul": "034",
    "izmir": "035",
}

# Sehir / meta bilgi kelimeleri (title'dan cikarilacak)
CITY_AND_META = [
    "ankara", "istanbul", "izmir", "antalya", "bursa", "kocaeli",
    "eskişehir", "konya", "adana", "mersin", "gaziantep", "kayseri",
    "romanya", "almanya",
    "(avr.)", "(asya)", "(tümü)",
    "iş yerinde", "hibrit", "uzaktan",
    "tam zamanlı", "yarı zamanlı", "part-time",
    "update", "gün", "saat", "hafta",
    "+", "il daha",
]


def _build_search_url(keyword, city=""):
    """Kariyer.net arama URL'si olusturur."""
    params = {"arama": keyword}
    if city and city.lower() in CITY_CODES:
        params["sehir"] = CITY_CODES[city.lower()]

    query_string = "&".join(
        f"{k}={quote(str(v))}" for k, v in params.items()
    )
    return f"{SEARCH_URL}?{query_string}"


def _clean_title(raw_title, company_name):
    """Ham baslik metnini temizler."""
    title = raw_title.strip()
    if not title:
        return ""

    # Firma adini birlesik metinden cikar
    if company_name and company_name in title:
        idx = title.index(company_name)
        title = title[:idx].strip()
    else:
        # Firma adi bulunamadiysa, kucuk->buyuk harf gecisinde kes
        match = re.search(r'[a-zığüşöçâî][A-ZİĞÜŞÖÇ]', title)
        if match and match.start() > 5:
            title = title[: match.start() + 1].strip()

    # Sehir/meta bilgilerini temizle
    title_lower = title.lower()
    for marker in CITY_AND_META:
        marker_lower = marker.lower()
        idx = title_lower.find(marker_lower)
        if idx > 0:
            title = title[:idx].strip()
            title_lower = title.lower()

    return title.strip()


def _extract_location(text):
    """Metinden sehir/lokasyon cikarir."""
    text_lower = text.lower()
    for city in ["ankara", "istanbul", "izmir", "antalya", "bursa", "kocaeli"]:
        if city in text_lower:
            return city.capitalize()
    if "uzaktan" in text_lower or "remote" in text_lower:
        return "Uzaktan"
    return ""


def _is_relevant(title, company):
    """Ilanin yazilim/muhendislik ile alakali olup olmadigini kontrol eder."""
    full_text = f"{title} {company}".lower()
    return any(kw.lower() in full_text for kw in RELEVANCE_KEYWORDS)


def _parse_cards_from_page(page, city):
    """Playwright page nesnesinden ilan kartlarini parse eder."""
    jobs = []
    seen_links = set()

    # Ilan kartlarini bul (JS render sonrasi)
    cards = page.query_selector_all("a.k-ad-card")

    if not cards:
        # Alternatif selectorler dene
        cards = page.query_selector_all("div[class*='listing'] a[href*='/is-ilani/']")

    for card in cards:
        try:
            href = card.get_attribute("href") or ""
            if not href or "/is-ilani/" not in href:
                continue
            if href in seen_links:
                continue

            full_url = href if href.startswith("http") else BASE_URL + href
            seen_links.add(href)

            # Firma adi – img alt attribute'undan
            img = card.query_selector("img[alt]")
            company = ""
            if img:
                company = (img.get_attribute("alt") or "").strip()

            # Sponsorlu ilan atlama
            card_html = card.inner_html()
            if "sponsored" in card_html.lower() or "sponsorlu" in card_html.lower():
                continue

            # Baslik – title-wrapper'dan veya genel text'ten
            title_el = card.query_selector("div.title-wrapper")
            if title_el:
                raw_title = title_el.inner_text().strip()
            else:
                raw_title = card.inner_text().strip()[:100]

            title = _clean_title(raw_title, company)
            if not title or len(title) < 3:
                continue

            # Relevance filtresi
            if not _is_relevant(title, company):
                continue

            # Lokasyon
            location = _extract_location(raw_title + " " + card.inner_text())
            city_label = city.capitalize() if city else "Turkiye"
            summary_location = location if location else city_label

            jobs.append({
                "title": title,
                "company": company,
                "link": full_url,
                "summary": summary_location,
                "published": datetime.now().strftime("%Y-%m-%d"),
                "source": "Kariyer.net",
            })

        except Exception:
            continue

    return jobs


def fetch_kariyer_search(page, search_config):
    """Playwright ile tek bir Kariyer.net aramasini ceker."""
    keyword = search_config["keyword"]
    city = search_config.get("city", "")
    city_label = city.capitalize() if city else "Turkiye"

    url = _build_search_url(keyword, city)

    print(f"  [KARIYER] '{keyword}' ({city_label}) araniyor... ", end="", flush=True)

    try:
        response = page.goto(url, timeout=30000)

        # 403 kontrolu
        if response and response.status == 403:
            print("[UYARI] Erisim engellendi (403)")
            return [], True

        # JS render bekleme – ilan kartlarinin yuklenmesini bekle
        try:
            page.wait_for_selector("a.k-ad-card", timeout=8000)
        except Exception:
            # Kartlar yuklenemediyse, sayfanin tamamen yuklenmesini bekle
            time.sleep(2)

        # Scroll ile lazy-load tetikle
        for _ in range(2):
            page.evaluate("window.scrollBy(0, 600)")
            time.sleep(random.uniform(0.3, 0.7))

        # Parse
        jobs = _parse_cards_from_page(page, city)
        print(f"[OK] {len(jobs)} ilan")
        return jobs, False

    except Exception as e:
        error_msg = str(e)
        if "403" in error_msg:
            print("[UYARI] Erisim engellendi (403)")
            return [], True
        print(f"[HATA] {error_msg[:80]}")
        return [], False


def fetch_all_kariyer_jobs():
    """Tum Kariyer.net aramalarini Playwright + Stealth ile ceker."""
    all_jobs = []
    seen_links = set()

    print("\n[INFO] Kariyer.net taraniyor (Playwright + Stealth)...\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[UYARI] Playwright yuklu degil – Kariyer.net atlaniyor.")
        return []

    # Stealth v2 API
    try:
        from playwright_stealth import Stealth
        stealth = Stealth()
        pw_context_manager = stealth.use_sync(sync_playwright())
    except ImportError:
        pw_context_manager = sync_playwright()

    try:
        with pw_context_manager as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="tr-TR",
            )
            page = context.new_page()

            # Once anasayfaya gidip cookie/session olustur
            try:
                page.goto("https://www.kariyer.net/", timeout=15000)
                time.sleep(random.uniform(2, 3))
            except Exception:
                pass

            for search in KARIYER_SEARCHES:
                jobs, blocked = fetch_kariyer_search(page, search)

                if blocked:
                    print("  [INFO] Kariyer.net erisim engellendi – kalan sorgular atlaniyor.\n")
                    break

                for job in jobs:
                    if job["link"] not in seen_links:
                        seen_links.add(job["link"])
                        all_jobs.append(job)

                # Aramalar arasi bekleme (anti-bot)
                delay = random.uniform(2, 4)
                time.sleep(delay)

            context.close()
            browser.close()

    except Exception as e:
        print(f"[HATA] Playwright browser hatasi: {e}")

    print(f"\n[INFO] Kariyer.net'ten toplam {len(all_jobs)} benzersiz ilan cekildi.\n")
    return all_jobs
