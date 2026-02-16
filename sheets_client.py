# sheets_client.py – Google Sheets Entegrasyon Modülü

import os
from datetime import datetime

from config import CREDENTIALS_FILE, SPREADSHEET_NAME, WORKSHEET_NAME

# Sheet başlık satırı
HEADERS = [
    "Tarih", "Firma", "Pozisyon", "Şehir", "Remote", "Kaynak",
    "Link", "Alan", "Level", "Alan Skoru", "Lokasyon Skoru",
    "Level Skoru", "Toplam Skor", "Başvuru", "DM", "Not",
]


def _get_sheet():
    """Google Sheets'e bağlanır ve worksheet döndürür."""
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except ImportError:
        print("⚠️  gspread veya google-auth yüklü değil. 'pip install gspread google-auth' çalıştırın.")
        return None

    if not os.path.exists(CREDENTIALS_FILE):
        print(f"⚠️  Credentials dosyası bulunamadı: {CREDENTIALS_FILE}")
        print("   Google Sheets'e yazmak için credentials.json dosyasını proje dizinine koyun.")
        return None

    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scopes)
        client = gspread.authorize(creds)

        try:
            spreadsheet = client.open(SPREADSHEET_NAME)
        except gspread.SpreadsheetNotFound:
            print(f"⚠️  Spreadsheet '{SPREADSHEET_NAME}' bulunamadı.")
            print("   Sheet'i oluşturup service account ile paylaşın.")
            return None

        # Worksheet'i bul veya oluştur
        try:
            worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        except gspread.WorksheetNotFound:
            worksheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=20)
            worksheet.append_row(HEADERS)
            print(f"  📝 '{WORKSHEET_NAME}' sayfası oluşturuldu.")

        return worksheet

    except Exception as e:
        print(f"❌ Google Sheets bağlantı hatası: {e}")
        return None


def get_existing_entries(worksheet):
    """Mevcut tüm kayıtları çeker (duplicate kontrol için)."""
    try:
        records = worksheet.get_all_values()
        if len(records) <= 1:  # sadece header var
            return [], set()

        # Link'leri topla (index 6 = Link kolonu)
        existing_links = set()
        existing_pairs = set()  # (firma, pozisyon) çiftleri

        for row in records[1:]:  # header'ı atla
            if len(row) > 6:
                existing_links.add(row[6].strip().lower())
            if len(row) > 2:
                pair = (row[1].strip().lower(), row[2].strip().lower())
                existing_pairs.add(pair)

        return existing_pairs, existing_links

    except Exception as e:
        print(f"⚠️  Mevcut kayıtlar okunamadı: {e}")
        return set(), set()


def is_duplicate(job, existing_pairs, existing_links):
    """İlanın daha önce eklenip eklenmediğini kontrol eder."""
    link = job.get("link", "").strip().lower()
    if link in existing_links:
        return True

    company = job.get("company", "").strip().lower()
    title = job.get("title", "").strip().lower()
    if company and title and (company, title) in existing_pairs:
        return True

    return False


def _is_remote(location):
    """Remote mu kontrol eder."""
    return location in ("remote", "hybrid_ankara")


def _format_city(location):
    """Lokasyonu Türkçe şehir formatına çevirir."""
    city_map = {
        "ankara": "Ankara",
        "remote": "",
        "hybrid_ankara": "Ankara",
        "türkiye": "Türkiye",
        "istanbul": "İstanbul",
        "diğer": "",
    }
    return city_map.get(location, "")


def append_jobs(jobs, worksheet=None):
    """
    Yeni ilanları Google Sheets'e ekler.
    worksheet=None ise bağlantı kurar.
    Döndürür: (eklenen_sayı, duplicate_sayı)
    """
    if worksheet is None:
        worksheet = _get_sheet()

    if worksheet is None:
        print("❌ Google Sheets'e bağlanılamadı. İlanlar eklenemedi.")
        return 0, 0

    existing_pairs, existing_links = get_existing_entries(worksheet)

    added = 0
    duplicates = 0
    rows_to_add = []

    for job in jobs:
        if is_duplicate(job, existing_pairs, existing_links):
            duplicates += 1
            continue

        row = [
            datetime.now().strftime("%Y-%m-%d"),       # Tarih
            job.get("company", ""),                     # Firma
            job.get("title", ""),                       # Pozisyon
            _format_city(job.get("location", "")),      # Şehir
            "✅" if _is_remote(job.get("location", "")) else "",  # Remote
            job.get("source", ""),                      # Kaynak
            job.get("link", ""),                        # Link
            job.get("field", ""),                       # Alan
            job.get("level", ""),                       # Level
            job.get("field_score", 0),                  # Alan Skoru
            job.get("location_score", 0),               # Lokasyon Skoru
            job.get("level_score", 0),                  # Level Skoru
            job.get("total_score", 0),                  # Toplam Skor
            "",                                         # Başvuru
            "",                                         # DM
            "",                                         # Not
        ]
        rows_to_add.append(row)
        added += 1

    # Toplu ekleme (API çağrısını minimize et)
    if rows_to_add:
        try:
            worksheet.append_rows(rows_to_add, value_input_option="USER_ENTERED")
            print(f"  ✅ {added} ilan Sheet'e eklendi.")
        except Exception as e:
            print(f"  ❌ Sheet'e yazma hatası: {e}")
            added = 0

    return added, duplicates
