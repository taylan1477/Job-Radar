# sheets_client.py – Google Sheets entegrasyonu

import re
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

from config import CREDENTIALS_FILE, SPREADSHEET_ID

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Header satiri (9 sutun – Kisitli kolonu kaldirildi)
HEADER = [
    "Başlık", "Firma", "Alan", "Lokasyon", "Level",
    "Skor", "Link", "Kaynak", "Tarih",
]


def _get_sheet():
    """Google Sheet worksheet nesnesini dondurur."""
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.sheet1

        # Header yoksa ekle
        first_row = worksheet.row_values(1)
        if not first_row:
            worksheet.append_row(HEADER, value_input_option="USER_ENTERED")

        return worksheet

    except Exception as e:
        print(f"[HATA] Google Sheets baglanti hatasi: {e}")
        return None


def get_existing_entries(worksheet=None):
    """Mevcut ilanların link listesini dondurur (duplicate kontrolu icin)."""
    if worksheet is None:
        worksheet = _get_sheet()
    if not worksheet:
        return set()

    try:
        records = worksheet.get_all_values()
        if len(records) <= 1:
            return set()

        # Link kolonu (index 7)
        existing_links = set()
        for row in records[1:]:
            if len(row) > 7 and row[7]:
                existing_links.add(row[7].strip())
        return existing_links

    except Exception as e:
        print(f"[HATA] Mevcut kayitlar okunamadi: {e}")
        return set()


def clear_sheet():
    """Sheet'teki tum verileri siler (header haric)."""
    worksheet = _get_sheet()
    if not worksheet:
        return False

    try:
        records = worksheet.get_all_values()
        if len(records) <= 1:
            print("  [INFO] Sheet zaten bos.")
            return True

        # Header disindaki tum satirlari sil
        row_count = len(records)
        if row_count > 1:
            worksheet.delete_rows(2, row_count)
            print(f"  [OK] {row_count - 1} satir silindi. Sheet temizlendi.")
        return True

    except Exception as e:
        print(f"[HATA] Sheet temizleme hatasi: {e}")
        return False


def append_jobs(jobs):
    """İlanlari Google Sheets'e toplu ekler. (eklenen, duplicate) tuple dondurur."""
    worksheet = _get_sheet()
    if not worksheet:
        return 0, 0

    existing = get_existing_entries(worksheet)
    rows_to_add = []
    duplicates = 0

    for job in jobs:
        link = job.get("link", "").strip()
        if not link or link in existing:
            duplicates += 1
            continue

        rows_to_add.append([
            job.get("title", ""),
            job.get("company", ""),
            job.get("field", "diğer"),
            job.get("location", ""),
            job.get("level", "bilinmiyor"),
            str(job.get("total_score", 0)).replace(".", ","),
            link,
            job.get("source", ""),
            job.get("published", ""),
        ])

    if not rows_to_add:
        return 0, duplicates

    try:
        worksheet.append_rows(rows_to_add, value_input_option="USER_ENTERED")
        print(f"  [OK] {len(rows_to_add)} satir toplu eklendi.")
    except Exception as e:
        print(f"  [HATA] Toplu ekleme basarisiz: {e}")
        return 0, duplicates

    return len(rows_to_add), duplicates


def _normalize_date(val):
    """Tarih degerini YYYY-MM-DD formatina cevirir. Saat kismini atar."""
    if not val or not val.strip():
        return ""
    val = val.strip()

    # 1) RFC 2822 formati: "Sun, 15 Feb 2026 10:30:52 GMT" veya "+0000"
    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(val)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    # 2) Saat kismini at (space veya T ile ayrilmis)
    #    "2026-02-16 14:30:00" -> "2026-02-16"
    #    "2026-02-16T10:30:00+03:00" -> "2026-02-16"
    date_only = re.split(r'[T ]', val)[0].strip()

    # Zaten YYYY-MM-DD mi?
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_only):
        return date_only

    # 3) Basit tarih formatlari (date_only uzerinde)
    for fmt in [
        "%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y",
        "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y",
    ]:
        try:
            return datetime.strptime(date_only, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    # 4) Tam string uzerinde (saat iceren formatlar)
    for fmt in [
        "%a, %d %b %Y %H:%M:%S %Z",    # Sun, 15 Feb 2026 10:30:52 GMT
        "%a, %d %b %Y %H:%M:%S %z",     # Mon, 19 Jan 2026 12:37:08 +0000
        "%a, %d %b %Y",                  # Sun, 15 Feb 2026
        "%d %b %Y",                      # 15 Feb 2026
        "%b %d, %Y",                     # Feb 15, 2026
        "%B %d, %Y",                     # February 15, 2026
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%d %H:%M:%S",
    ]:
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    # 5) ISO format (timezone dahil)
    try:
        return datetime.fromisoformat(val).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    return date_only if date_only != val else val


def fix_sheet():
    """
    Mevcut Sheet tablosunu duzeltir ve yeniden skorlar:
    1. Basliklari yazar
    2. Bos sutunlari siler (Kisitli + 11-16)
    3. Tarihleri YYYY-MM-DD formatina cevirir
    4. Ilanları yeniden skorlar (config.py degisiklikleri icin)
    """
    from scorer import detect_field, detect_location, detect_level, calculate_score

    worksheet = _get_sheet()
    if not worksheet:
        return False

    try:
        all_data = worksheet.get_all_values()
        if not all_data:
            print("  [INFO] Sheet bos, duzeltilecek bir sey yok.")
            return True

        print(f"  [INFO] {len(all_data)} satir, {len(all_data[0])} sutun okundu.")

        # --- Adim 1: Bos sutunlari bul ---
        num_cols = max(len(row) for row in all_data)
        data_rows = all_data[1:] if len(all_data) > 1 else []
        empty_cols = set()
        for col_idx in range(num_cols):
            all_empty = True
            for row in data_rows:
                if col_idx < len(row) and row[col_idx].strip():
                    all_empty = False
                    break
            if all_empty:
                empty_cols.add(col_idx)

        if empty_cols:
            print(f"  [INFO] Bos sutunlar (0-indexed): {sorted(empty_cols)}")

        # --- Adim 2: Bos sutunlari kaldir ---
        keep_cols = [i for i in range(num_cols) if i not in empty_cols]

        cleaned_data = []
        for row_idx, row in enumerate(all_data):
            new_row = []
            for col_idx in keep_cols:
                val = row[col_idx] if col_idx < len(row) else ""
                new_row.append(val)
            cleaned_data.append(new_row)

        # --- Adim 2.5: Tarih sutununu bul ve normalize et ---
        # Header'dan "Tarih" sutununu bul (dinamik)
        header_row = cleaned_data[0] if cleaned_data else []
        date_col_idx = -1
        for idx, col_name in enumerate(header_row):
            if col_name.strip().lower() in ("tarih", "date"):
                date_col_idx = idx
                break
        # Header'da bulunamadiysa, HEADER listesinden bul
        if date_col_idx == -1:
            try:
                date_col_idx = HEADER.index("Tarih")
            except ValueError:
                date_col_idx = len(HEADER) - 1  # Son sutun

        print(f"  [INFO] Tarih sutunu: index {date_col_idx}")

        # Tarihleri normalize et
        date_fixed = 0
        for row_idx in range(1, len(cleaned_data)):
            row = cleaned_data[row_idx]
            if date_col_idx < len(row):
                old_val = row[date_col_idx]
                new_val = _normalize_date(old_val)
                if old_val != new_val:
                    row[date_col_idx] = new_val
                    date_fixed += 1

        print(f"  [INFO] {date_fixed} tarih normalize edildi.")

        # --- Adim 3: Header'i dogru yaz ---
        max_used = len(HEADER)
        final_data = [HEADER]
        for row in cleaned_data[1:]:
            final_data.append(row[:max_used])

        # --- Adim 4: Yeniden skorlama ---
        # Sutun indices (temiz): Baslik=0, Firma=1, Alan=2, Lokasyon=3, Level=4, Skor=5, Link=6, Kaynak=7, Tarih=8
        changed = {"alan": 0, "lokasyon": 0, "level": 0, "skor": 0}
        for i in range(1, len(final_data)):
            row = final_data[i]
            if len(row) < max_used:
                row.extend([""] * (max_used - len(row)))

            title = row[0]
            company = row[1]
            existing_field = row[2]     # Mevcut alan (scraper'dan)
            existing_location = row[3]  # Mevcut lokasyon (scraper'dan)
            source = row[7] if len(row) > 7 else ""

            # Tum mevcut bilgileri birlestir
            full_text = f"{title} {company} {existing_location} {existing_field} {source}"

            new_field = detect_field(full_text)
            new_location = detect_location(full_text)
            new_level = detect_level(full_text)
            new_score = calculate_score(new_field, new_location, new_level)

            if row[2] != new_field:
                changed["alan"] += 1
            if row[3] != new_location:
                changed["lokasyon"] += 1
            if row[4] != new_level:
                changed["level"] += 1
            score_str = str(new_score).replace(".", ",")
            if row[5] != score_str:
                changed["skor"] += 1

            row[2] = new_field
            row[3] = new_location
            row[4] = new_level
            row[5] = score_str

            final_data[i] = row

        total_cells = sum(changed.values()) + date_fixed
        print(f"\n  --- Degisiklik Ozeti ---")
        print(f"  Alan    : {changed['alan']} hucre")
        print(f"  Lokasyon: {changed['lokasyon']} hucre")
        print(f"  Level   : {changed['level']} hucre")
        print(f"  Skor    : {changed['skor']} hucre")
        print(f"  Tarih   : {date_fixed} hucre")
        print(f"  TOPLAM  : {total_cells} hucre degisti\n")

        # --- Adim 5: Sheet'i guncelle ---
        removed_cols = num_cols - max_used
        print(f"  [INFO] {removed_cols} bos sutun siliniyor, {max_used} sutun kalacak.")
        print(f"  [INFO] Basliklar: {HEADER}")

        worksheet.clear()
        worksheet.update(f"A1:{chr(64 + max_used)}{len(final_data)}",
                         final_data, value_input_option="USER_ENTERED")

        sheet_cols = worksheet.col_count
        if sheet_cols > max_used:
            worksheet.delete_columns(max_used + 1, sheet_cols)

        print(f"  [OK] Tablo duzeltildi: {len(final_data)-1} satir, {max_used} sutun.")
        return True

    except Exception as e:
        print(f"[HATA] Tablo duzeltme hatasi: {e}")
        return False

