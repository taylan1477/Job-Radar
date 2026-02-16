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
            str(job.get("total_score", 0)),
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
    """Tarih degerini YYYY-MM-DD formatina cevirir."""
    if not val or not val.strip():
        return ""
    val = val.strip()

    # Zaten dogru formatta mi?
    if re.match(r'^\d{4}-\d{2}-\d{2}$', val):
        return val

    # Bilinen formatları dene
    for fmt in [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d.%m.%Y",
        "%b %d, %Y",   # Jan 15, 2026
        "%B %d, %Y",   # January 15, 2026
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
    ]:
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    # ISO formatini dene (2026-02-16T10:30:00+03:00)
    try:
        return datetime.fromisoformat(val).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    return val  # Donusturulemezse olduğu gibi birak


def fix_sheet():
    """
    Mevcut Sheet tablosunu duzeltir:
    1. Basliklari yazar
    2. Bos sutunlari siler (Kisitli + 11-16)
    3. Tarihleri YYYY-MM-DD formatina cevirir
    """
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
        # Bir sutun tamamen bos mu? (header haric)
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

        # --- Adim 2: Bos sutunlari kaldir + tarihleri normalize et ---
        keep_cols = [i for i in range(num_cols) if i not in empty_cols]

        # Tarih sutunu: son tutulan kolon olacak (index 9 veya son)
        # Asil tarih sutun indeksi: orijinal 10. sutun = index 9
        date_col_original = 9  # 0-indexed

        cleaned_data = []
        for row_idx, row in enumerate(all_data):
            new_row = []
            for col_idx in keep_cols:
                val = row[col_idx] if col_idx < len(row) else ""
                # Tarih normalizasyonu (header degilse)
                if col_idx == date_col_original and row_idx > 0:
                    val = _normalize_date(val)
                new_row.append(val)
            cleaned_data.append(new_row)

        # --- Adim 3: Header'i dogru yaz ---
        # Keep_cols sayisi HEADER ile uyusmayabilir, eslestirelim
        if len(keep_cols) >= len(HEADER):
            cleaned_data[0] = HEADER + [""] * (len(keep_cols) - len(HEADER))
        else:
            cleaned_data[0] = HEADER[:len(keep_cols)]

        # Fazla bos sutunlari kirp (her satirda sondaki boslari sil)
        max_used = len(HEADER)
        final_data = []
        for row in cleaned_data:
            final_data.append(row[:max_used])

        # --- Adim 4: Sheet'i guncelle ---
        removed_cols = num_cols - max_used
        print(f"  [INFO] {removed_cols} bos sutun siliniyor, {max_used} sutun kalacak.")
        print(f"  [INFO] Basliklar: {HEADER}")

        # Tum sheet'i temizle ve yeniden yaz
        worksheet.clear()
        worksheet.update(f"A1:{chr(64 + max_used)}{len(final_data)}",
                         final_data, value_input_option="USER_ENTERED")

        # Fazla sutunlari sil (eger varsa)
        sheet_cols = worksheet.col_count
        if sheet_cols > max_used:
            worksheet.delete_columns(max_used + 1, sheet_cols)

        print(f"  [OK] Tablo duzeltildi: {len(final_data)-1} satir, {max_used} sutun.")
        return True

    except Exception as e:
        print(f"[HATA] Tablo duzeltme hatasi: {e}")
        return False
