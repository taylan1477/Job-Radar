# sheets_client.py – Google Sheets entegrasyonu

import sys
import io
import re
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials
from gspread_formatting import format_cell_range, cellFormat, textFormat, numberFormat
from gspread.utils import rowcol_to_a1

from src.utils.config import CREDENTIALS_FILE, SPREADSHEET_ID

# Windows konsol encoding fix
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions (<3.7)
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Header satiri (9 sutun – Kaynak kaldirildi, Durum index 8)
HEADER = [
    "Başlık", "Firma", "Alan", "Lokasyon", "Level",
    "Skor", "Link", "Tarih", "Durum",
]

# Domain -> Kisa isim eslesmesi
DOMAIN_LABELS = {
    "linkedin.com": "LinkedIn",
    "weworkremotely.com": "WWRemotely",
    "himalayas.app": "Himalayas",
    "kariyer.net": "Kariyer",
    "indeed.com": "Indeed",
    "glassdoor.com": "Glassdoor",
    "monster.com": "Monster",
    "dice.com": "Dice",
    "github.com": "GitHub",
    "stackoverflow.com": "StackOverflow",
    "remoteok.com": "RemoteOK",
    "wellfound.com": "Wellfound",
}

STATUS_OPTIONS = [
    "Favori",
    "Başvuruldu",
    "Reddedildi",
    "Görüşmede",
    "Mülakat",
    "İşe Alındı",
    "Süre Bitti",
    "Ulaşılamaz",
]


def _make_hyperlink(url):
    """URL'yi =HYPERLINK("url"; "Label") formulune cevirir. (TR locale icin ; ayrac)"""
    if not url or not url.strip():
        return ""
    url = url.strip()
    if url.upper().startswith("=HYPERLINK"):
        return url

    label = "Link"
    url_lower = url.lower()
    for domain, name in DOMAIN_LABELS.items():
        if domain in url_lower:
            label = name
            break

    safe_url = url.replace('"', '%22')
    return f'=HYPERLINK("{safe_url}"; "{label}")'


def _extract_url(cell_value):
    """Hucre degerinden URL'yi cikarir."""
    if not cell_value:
        return ""
    cell_value = cell_value.strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', cell_value, re.IGNORECASE)
    if m:
        return m.group(1)
    return cell_value


def _get_sheet():
    """Google Sheet worksheet nesnesini dondurur."""
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sh.sheet1

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
        records = worksheet.get_all_values(value_render_option="FORMULA")
        if len(records) <= 1:
            return set()

        # Link kolonu (yeni index 6, eski tablolarda farkli olabilir ama fix_sheet sonrasi 6 olacak)
        # Guvenli olmak icin header kontrolu yapilabilir ama burada basite kaciyoruz
        # Simdilik 6. indekse (bazen 7 olabilir eski veride) bakalim
        
        # Header'i bul
        header = records[0]
        link_idx = -1
        for i, h in enumerate(header):
            if h.strip().lower() == "link":
                link_idx = i
                break
        
        if link_idx == -1:
            link_idx = 6  # Varsayilan

        existing_links = set()
        for row in records[1:]:
            if len(row) > link_idx and row[link_idx]:
                url = _extract_url(row[link_idx])
                if url:
                    existing_links.add(url)
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

        # Kaynak (source) artalana yazilmiyor
        rows_to_add.append([
            job.get("title", ""),
            job.get("company", ""),
            job.get("field", "diğer"),
            job.get("location", ""),
            job.get("level", "bilinmiyor"),
            str(job.get("total_score", 0)).replace(".", ","),
            _make_hyperlink(link),
            job.get("published", ""), # Tarih
            "",  # Durum (bos birakilir, dropdown kullanici sececek)
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
    if not val or not val.strip():
        return ""
    val = val.strip()

    if val.isdigit() and len(val) == 5:
        try:
            from datetime import timedelta
            dt = datetime(1899, 12, 30) + timedelta(days=int(val))
            return dt.strftime("%Y-%m-%d")
        except:
            pass

    try:
        from email.utils import parsedate_to_datetime
        dt = parsedate_to_datetime(val)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        pass

    date_only = re.split(r'[T ]', val)[0].strip()
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_only):
        return date_only

    for fmt in ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d", "%d.%m.%Y"]:
        try:
            return datetime.strptime(date_only, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
            
    try:
        return datetime.fromisoformat(val).strftime("%Y-%m-%d")
    except:
        pass

    return date_only if date_only != val else val


def format_columns(worksheet, num_rows):
    """Sutunlara display formati ve validation uygular."""
    if num_rows < 2:
        return

    try:
        # H (Tarih) kolonunu (index 7, 1-based index 8) Date formatina zorla
        # A1 notasyonunda H2:H{num_rows}
        date_range = f"H2:H{num_rows}"
        format_cell_range(worksheet, date_range, cellFormat(
            numberFormat=numberFormat(type='DATE', pattern='yyyy-mm-dd')
        ))
        print("  [INFO] Tarih kolonu (H) formatlandi: yyyy-mm-dd")

        # F (Skor) kolonunu (index 5, 1-based index 6) Number formatina zorla
        score_range = f"F2:F{num_rows}"
        format_cell_range(worksheet, score_range, cellFormat(
            numberFormat=numberFormat(type='NUMBER', pattern='#,##0.0')
        ))
        
        # Validation for Status (I column, index 8)
        set_status_validation(worksheet, num_rows)
        
        # Row coloring based on Status (Conditional Formatting)
        apply_conditional_formatting(worksheet, num_rows)
        
    except Exception as e:
        print(f"  [UYARI] Formatlama hatasi: {e}")


def apply_conditional_formatting(worksheet, num_rows):
    """Satirlari durum degerine gore renklendirir."""
    if num_rows < 2:
        return

    try:
        # Renk Tanimlari (RGB 0.0 - 1.0)
        # Daha profesyonel, göz yormayan pastel tonlar
        # Soft Rose / Muted Red: Daha açık ama doymuş bir ton.
        # Okunabilirliği artırır, "alarm" gibi parlamaz.
        color_red = {"red": 0.35, "green": 0.15, "blue": 0.15}
        # Sage Green: Griye yakın, çok yumuşak bir yeşil.
        # Uzun süre bakıldığında gözü en az yoran tondur.
        color_pale_green = {"red": 0.22, "green": 0.32, "blue": 0.25}
        # Muted Amber: Turuncuya kaçmayan, saman rengi bir sarı.
        color_yellow = {"red": 0.35, "green": 0.30, "blue": 0.15}

        # Emerald Forest: Biraz daha derinliği olan, güven veren bir yeşil.
        color_bright_green = {"red": 0.12, "green": 0.28, "blue": 0.20}
        # Durum Gecerlilik Listesi (Spelling kontrolu)
        # Red: "Reddedildi", "Ulaşılamaz", "Süre Bitti"
        # Pale Green: "Başvuruldu"
        # Yellow: "Favori"
        # Bright Green: "İşe Alındı", "Mülakat", "Görüşmede"

        requests = []
        
        # Onceki kurallari temizle (Batch update ile her seferinde sifirdan eklemek yerine)
        # Gspread-formatting'in boyle bir yetenegi var mi bakilmali ama manuel batchUpdate daha kesin.
        
        # Kosullu bicimlendirmeleri silmek icin (ilgili sheet'teki tum kurallari sil)
        # Bu biraz karmasik (index bilmek lazim). 
        # Simdilik sadece ekleyelim, cok birikirse temizlik gerekir.

        def add_single_rule(status, color):
            # En basit kural: =$I2="Durum"
            # Locale bagimliligi ihtimaline karsi en sade hali
            formula = f'=$I2="{status}"'
            return {
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": worksheet.id,
                            "startRowIndex": 1,
                            "endRowIndex": num_rows,
                            "startColumnIndex": 0,
                            "endColumnIndex": 9
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "CUSTOM_FORMULA",
                                "values": [{"userEnteredValue": formula}]
                            },
                            "format": {
                                "backgroundColor": color
                            }
                        }
                    },
                    "index": 0
                }
            }

        # Kurallari sirayla ekle (Index: 0 her seferinde en uste ekler)
        # Kirmizi Grup
        for s in ["Reddedildi", "Ulaşılamaz", "Süre Bitti"]:
            requests.append(add_single_rule(s, color_red))
        
        # Basvuruldu
        requests.append(add_single_rule("Başvuruldu", color_pale_green))
        
        # Favori
        requests.append(add_single_rule("Favori", color_yellow))
        
        # Yesil Grup
        for s in ["İşe Alındı", "Mülakat", "Görüşmede"]:
            requests.append(add_single_rule(s, color_bright_green))

        worksheet.spreadsheet.batch_update({"requests": requests})
        print(f"  [INFO] Satir renklendirme kurallari (Individual Rules) uygulandi.")

    except Exception as e:
        print(f"  [UYARI] Renklendirme hatasi: {e}")


def set_status_validation(worksheet, num_rows):
    """Durum kolonuna (I) Smart Chip dropdown validation ekler."""
    if num_rows < 2:
        return
        
    try:
        # I kolonu (Index 8) -> Durum
        start_row = 1  # 0-indexed, skip header (row 0) -> row 1 is data start
        end_row = num_rows # non-inclusive or inclusive? API usually non-inclusive for end index? No, it's endRowIndex.
        
        # Google Sheets API v4 DataValidation
        # Durum kolonuna Dropdown (Smart Chip stili)
        
        requests = [{
            "setDataValidation": {
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": 1,
                    "endRowIndex": num_rows,
                    "startColumnIndex": 8,
                    "endColumnIndex": 9
                },
                "rule": {
                    "condition": {
                        "type": "ONE_OF_LIST",
                        "values": [{"userEnteredValue": v} for v in STATUS_OPTIONS]
                    },
                    "showCustomUi": True, # Dropdown goster
                    "strict": True
                }
            }
        }]
        
        worksheet.spreadsheet.batch_update({"requests": requests})
        print(f"  [INFO] Durum kolonuna (I) Dropdown validation eklendi.")
        
    except Exception as e:
        print(f"  [UYARI] Validation ekleme hatasi: {e}")


def fix_sheet():
    """
    Mevcut Sheet tablosunu duzeltir:
    1. 'Kaynak' sutununu kaldirir (veya gormezden gelir).
    2. Yeni header yapisina (9 sutun) cevirir.
    3. Tarih ve Skor formatlarini duzeltir.
    4. Linkleri duzeltir.
    5. Durum sutununu korur ve Dropdown ekler.
    """
    from src.core.scorer import detect_field, detect_location, detect_level, calculate_score

    worksheet = _get_sheet()
    if not worksheet:
        return False

    try:
        raw_data = worksheet.get_all_values(value_render_option="FORMULA")
        if not raw_data:
            print("  [INFO] Sheet bos.")
            return True

        # FORMULA modu sayilari float yapabilir, str'ye cevir
        all_data = [[str(cell) if not isinstance(cell, str) else cell for cell in row] for row in raw_data]

        print(f"  [INFO] Okunan veri: {len(all_data)} satir, {len(all_data[0])} sutun.")

        # --- Eski kolonlari tespit et ---
        old_header = all_data[0]
        # Kolon mapping
        # Beklenen: Baslik, Firma, Alan, Lokasyon, Level, Skor, Link, [Kaynak], Tarih, Durum
        
        col_map = {
            "Baslik": -1, "Firma": -1, "Alan": -1, "Lokasyon": -1, "Level": -1,
            "Skor": -1, "Link": -1, "Tarih": -1, "Durum": -1
        }
        
        for i, h in enumerate(old_header):
            h_lower = h.strip().lower()
            if "başlık" in h_lower or "title" in h_lower: col_map["Baslik"] = i
            elif "firma" in h_lower or "company" in h_lower: col_map["Firma"] = i
            elif "alan" in h_lower or "field" in h_lower: col_map["Alan"] = i
            elif "lokasyon" in h_lower or "location" in h_lower: col_map["Lokasyon"] = i
            elif "level" in h_lower: col_map["Level"] = i
            elif "skor" in h_lower or "score" in h_lower: col_map["Skor"] = i
            elif "link" in h_lower: col_map["Link"] = i
            elif "tarih" in h_lower or "date" in h_lower: col_map["Tarih"] = i
            elif "durum" in h_lower or "status" in h_lower: col_map["Durum"] = i

        # Eger Link bulunamadiysa varsayilan 6
        if col_map["Link"] == -1: col_map["Link"] = 6
        
        # --- Durum haritasi (Link -> Durum) ---
        durum_map = {}
        durum_idx = col_map["Durum"]
        link_idx = col_map["Link"]
        
        if durum_idx != -1 and link_idx != -1:
            for row in all_data[1:]:
                if len(row) > link_idx and len(row) > durum_idx:
                    link_val = row[link_idx]
                    durum_val = row[durum_idx]
                    url = _extract_url(link_val)
                    if url and durum_val.strip():
                        # Status values mapping (eski text'leri yeni dropdown'a uydur)
                        # or just keep as is, validation might complain but data stays
                        durum_map[url] = durum_val.strip()
                        
        print(f"  [INFO] {len(durum_map)} durum kaydı hafızaya alındı.")

        # --- YENI veriyi olustur ---
        new_data = [HEADER]
        
        for i, row in enumerate(all_data[1:]):
            # Eski row'dan verileri cek
            def get_val(key, default=""):
                idx = col_map.get(key, -1)
                if idx != -1 and idx < len(row):
                    return row[idx]
                # Fallback: eger map yoksa indeksle dene (riskli ama bos donmekten iyidir)
                # Yeni siraya gore degil eski siraya gore tahmin:
                # 0:Title, 1:Comp, 2:Field, 3:Loc, 4:Lvl, 5:Score, 6:Link, 7:Source, 8:Date, 9:Status
                fallback_idxs = {
                    "Baslik": 0, "Firma": 1, "Alan": 2, "Lokasyon": 3, "Level": 4, 
                    "Skor": 5, "Link": 6, "Tarih": 8
                }
                fb_idx = fallback_idxs.get(key, -1)
                if fb_idx != -1 and fb_idx < len(row):
                    return row[fb_idx]
                return default

            title = get_val("Baslik")
            company = get_val("Firma")
            source_val = "" # Kaynak artik yok ama skorda kullaniliyordu
            # Kaynak eski row[7] olabilir
            if len(row) > 7: source_val = row[7] 
            
            # Yeniden skorlamak icin metin (Kaynak dahil degil artik veya sadece text olarak)
            # detect_field vs fonksiyonlari text bazli
            full_text = f"{title} {company} {get_val('Lokasyon')} {get_val('Alan')} {source_val}"
            
            new_field = detect_field(full_text)
            new_location = detect_location(full_text)
            new_level = detect_level(full_text)
            new_score = calculate_score(new_field, new_location, new_level)
            
            link_raw = get_val("Link")
            url = _extract_url(link_raw)
            new_link = _make_hyperlink(url)
            
            # Tarih
            raw_date = get_val("Tarih")
            new_date = _normalize_date(raw_date)
            
            # Durum
            status = ""
            if url in durum_map:
                status = durum_map[url]
            
            new_row = [
                title,
                company,
                new_field,
                new_location,
                new_level,
                str(new_score).replace(".", ","),
                new_link,
                new_date,
                status
            ]
            new_data.append(new_row)

        print(f"  [INFO] Yeni tablo hazirlandi: {len(new_data)} satir.")

        # --- Sheet'i temizle ve yaz ---
        worksheet.clear()
        
        # 9 sutun (I)
        last_col = "I"
        worksheet.update(f"A1:{last_col}{len(new_data)}",
                         new_data, value_input_option="USER_ENTERED")

        # Fazla sutunlari sil
        if worksheet.col_count > 9:
            worksheet.delete_columns(10, worksheet.col_count)

        # Format ve Validation
        format_columns(worksheet, len(new_data))
        
        print(f"  [OK] Tablo guncellendi (Kaynak silindi, Durum validasyonu eklendi).")
        return True

    except Exception as e:
        print(f"[HATA] Tablo duzeltme hatasi: {e}")
        import traceback
        traceback.print_exc()
        return False
