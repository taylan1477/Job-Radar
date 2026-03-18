import re
import gspread
from google.oauth2.service_account import Credentials
from src.utils.config import CREDENTIALS_FILE

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

def extract_sheet_id(url):
    m = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if m:
        return m.group(1)
    return url.strip()

def _extract_url(cell_value):
    if not cell_value: return ""
    cell_value = str(cell_value).strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', cell_value, re.IGNORECASE)
    if m: return m.group(1)
    return cell_value

def get_col_map(header):
    cmap = {"Baslik": -1, "Firma": -1, "Link": -1, "Durum": -1}
    for i, h in enumerate(header):
        hl = str(h).strip().lower()
        if "başlık" in hl or "title" in hl: cmap["Baslik"] = i
        elif "firma" in hl or "company" in hl: cmap["Firma"] = i
        elif "link" in hl: cmap["Link"] = i
        elif "durum" in hl or "status" in hl: cmap["Durum"] = i
    if cmap["Link"] == -1: cmap["Link"] = 6
    if cmap["Durum"] == -1: cmap["Durum"] = 8
    return cmap

def main():
    print("="*60)
    print("  Job Radar - Tablo Durum Birlestirici & Eksik Ilan Aktarici")
    print("="*60)
    
    old_url = input("1. Eski (Durumlarin dolu oldugu) Google Sheets URL'si veya ID'si:\n> ")
    new_url = input("\n2. Yeni (Durumlarin BOS oldugu) Google Sheets URL'si veya ID'si:\n> ")

    old_id = extract_sheet_id(old_url)
    new_id = extract_sheet_id(new_url)

    if not old_id or not new_id:
        print("[HATA] Gecerli ID bulunamadi.")
        return

    print("\n[INFO] Baglanti kuruluyor...")
    try:
        creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(creds)
    except Exception as e:
        print(f"[HATA] Hizmet hesabina baglanilamadi: {e}")
        return

    try:
        print("[INFO] Eski tablo okunuyor...")
        old_sh = gc.open_by_key(old_id)
        old_ws = old_sh.sheet1
        old_data = old_ws.get_all_values(value_render_option="FORMULA")
    except Exception as e:
        print(f"[HATA] Eski tablo okunamadi: {e}")
        return

    try:
        print("[INFO] Yeni tablo okunuyor...")
        new_sh = gc.open_by_key(new_id)
        new_ws = new_sh.sheet1
        new_data = new_ws.get_all_values(value_render_option="FORMULA")
    except Exception as e:
        print(f"[HATA] Yeni tablo okunamadi: {e}")
        return

    print(f"\n  > Eski tablo satır sayısı: {len(old_data)}")
    print(f"  > Yeni tablo satır sayısı: {len(new_data)}")

    # 1. Yeni tablodaki (var olan) kayitlarin ID'lerini topla
    new_cmap = get_col_map(new_data[0] if new_data else [])
    new_d_idx = new_cmap["Durum"]
    if new_d_idx == -1:
        print("[HATA] Yeni tabloda Durum sutunu bulunamadi.")
        return

    new_urls = set()
    new_tcs = set()
    
    for row in new_data[1:]:
        link_idx = new_cmap["Link"]
        t_idx = new_cmap["Baslik"]
        c_idx = new_cmap["Firma"]
        
        url = _extract_url(row[link_idx]) if link_idx != -1 and len(row) > link_idx else ""
        t = row[t_idx].strip().lower() if t_idx != -1 and len(row) > t_idx else ""
        c = row[c_idx].strip().lower() if c_idx != -1 and len(row) > c_idx else ""
        
        if url: 
            new_urls.add(url)
            new_urls.add(url.split("?")[0])
        if t: 
            new_tcs.add(f"{t}|{c}")

    # 2. Eski tablodaki Durum'u olan satirlari tara
    old_cmap = get_col_map(old_data[0] if old_data else [])
    
    rows_to_append = []
    durum_map = {}
    tc_map = {}
    
    for row in old_data[1:]:
        d_idx = old_cmap["Durum"]
        if d_idx != -1 and len(row) > d_idx:
            status = row[d_idx].strip()
            if status:
                # Durum var! Bu satir yeni tabloda var mi?
                link_idx = old_cmap["Link"]
                t_idx = old_cmap["Baslik"]
                c_idx = old_cmap["Firma"]
                
                url = _extract_url(row[link_idx]) if link_idx != -1 and len(row) > link_idx else ""
                t = row[t_idx].strip().lower() if t_idx != -1 and len(row) > t_idx else ""
                c = row[c_idx].strip().lower() if c_idx != -1 and len(row) > c_idx else ""
                
                base_url = url.split("?")[0] if url else ""
                tc_key = f"{t}|{c}"
                
                exists_in_new = False
                if url and url in new_urls: 
                    exists_in_new = True
                elif base_url and base_url in new_urls: 
                    exists_in_new = True
                elif tc_key and t and c and tc_key in new_tcs: 
                    exists_in_new = True
                
                # Check if it was really found update the maps, else append
                if exists_in_new:
                    # Yeni tabloda var, guncelleme verisi icin hafizaya al
                    if url: 
                        durum_map[url] = status
                        durum_map[base_url] = status
                    if t:
                        tc_map[tc_key] = status
                else:
                    # Yeni tabloda YOK! Append listesine ekle.
                    # Yeni tablonun header yapisina uygun bir satir olusturalim
                    new_row = [""] * len(new_data[0])
                    # Verileri eslestirip kopyala
                    for key, idx in old_cmap.items():
                        new_idx = new_cmap.get(key, -1)
                        if idx != -1 and new_idx != -1 and len(row) > idx:
                            new_row[new_idx] = row[idx]
                    
                    # Eski tabloda var olup map'lenemeyen ek sutunlar olabilir. Ozetle "Header ile eslesen her seyi" al:
                    # Alternatif tam karsilastirarak eskiyi yeniye cevirme
                    for h_idx, h_name in enumerate(new_data[0]):
                        # Eski tabloda bu header'in indexini bul
                        for o_idx, o_name in enumerate(old_data[0]):
                            if str(h_name).strip().lower() == str(o_name).strip().lower():
                                if len(row) > o_idx:
                                    new_row[h_idx] = row[o_idx]
                                break
                    
                    # Bos listeleri string'e float'lari stringe cevir -> USER_ENTERED format uyarilari vermesin
                    clean_row = [str(x) if x is not None else "" for x in new_row]
                    rows_to_append.append(clean_row)

    print(f"\n[INFO] Eski tablodan yeni tabloda BULUNMAYAN {len(rows_to_append)} adet 'Durum' isaretli ilan tespit edildi.")
    print(f"[INFO] Yeni tabloda var olan {len(durum_map)} farkli linkten guncelleme verisi yakalandi.")

    # 3. Yeni tablodaki mevcut satirlari GUNCELLE
    status_col_letter = chr(65 + new_d_idx) if new_d_idx < 26 else "I" 
    updated_count = 0
    updates = []
    
    for idx, row in enumerate(new_data[1:], start=2): # +1 pass header, +1 for 1-based index
        current_status = row[new_d_idx].strip() if len(row) > new_d_idx else ""
        
        link_idx = new_cmap["Link"]
        t_idx = new_cmap["Baslik"]
        c_idx = new_cmap["Firma"]
        
        url = _extract_url(row[link_idx]) if link_idx != -1 and len(row) > link_idx else ""
        t = row[t_idx].strip().lower() if t_idx != -1 and len(row) > t_idx else ""
        c = row[c_idx].strip().lower() if c_idx != -1 and len(row) > c_idx else ""
        
        recovered_status = ""
        base_url = url.split("?")[0] if url else ""
        tc_key = f"{t}|{c}"
        
        if url in durum_map: recovered_status = durum_map[url]
        elif base_url and base_url in durum_map: recovered_status = durum_map[base_url]
        elif tc_key in tc_map: recovered_status = tc_map[tc_key]
        
        # Eger mevcut durum bossa veya kurtarilanla farkliysa, uzerine yaz
        if recovered_status and current_status != recovered_status:
            updates.append({'range': f'{status_col_letter}{idx}', 'values': [[recovered_status]]})
            updated_count += 1

    if updates:
        print(f"\n[INFO] Yeni tabloda {updated_count} kaydin Durum degeri guncelleniyor...")
        new_ws.batch_update(updates, value_input_option="USER_ENTERED")
        print("[OK] Guncellemeler tamamlandi.")
    else:
        print("\n[INFO] Yeni tabloda guncellenecek isaretsiz ilan bulunamadi.")

    # 4. Eksik satirlari APPEND et
    if rows_to_append:
        print(f"\n[INFO] Yeni tabloya eksik olan {len(rows_to_append)} eski isaretli ilan EKLENIYOR...")
        new_ws.append_rows(rows_to_append, value_input_option="USER_ENTERED")
        print("[OK] Eksik kayitlar basariyla eklendi!")

    print("\n[BITTI] Tum islemler tamamladi.")

if __name__ == "__main__":
    main()
