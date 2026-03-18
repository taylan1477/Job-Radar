import re
def _extract_url(cell_value):
    if not cell_value: return ""
    cell_value = str(cell_value).strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', cell_value, re.IGNORECASE)
    if m: return m.group(1)
    return cell_value

def simulate():
    old_header = ["Başlık", "Firma", "Alan", "Lokasyon", "Level", "Skor", "Link", "Tarih", "Durum"]
    all_data = [
        old_header,
        ["Job1", "C1", "F1", "L1", "L", "4", '=HYPERLINK("https://linkedin.com/j1"; "L")', "2023-01-01", "Favori"],
        ["Job2", "C2", "F2", "L2", "L", "3", '=HYPERLINK("https://linkedin.com/j2"; "L")', "2023-01-02", ""]
    ]
    
    col_map = {k: -1 for k in ["Baslik", "Firma", "Alan", "Lokasyon", "Level", "Skor", "Link", "Tarih", "Durum"]}
    for i, h in enumerate(old_header):
        h_lower = str(h).strip().lower()
        if "başlık" in h_lower or "title" in h_lower: col_map["Baslik"] = i
        elif "firma" in h_lower or "company" in h_lower: col_map["Firma"] = i
        elif "alan" in h_lower or "field" in h_lower: col_map["Alan"] = i
        elif "lokasyon" in h_lower or "location" in h_lower: col_map["Lokasyon"] = i
        elif "level" in h_lower: col_map["Level"] = i
        elif "skor" in h_lower or "score" in h_lower: col_map["Skor"] = i
        elif "link" in h_lower: col_map["Link"] = i
        elif "tarih" in h_lower or "date" in h_lower: col_map["Tarih"] = i
        elif "durum" in h_lower or "status" in h_lower: col_map["Durum"] = i
        
    durum_map = {}
    durum_idx = col_map["Durum"]
    link_idx = col_map["Link"]
    print("durum_idx:", durum_idx, "link_idx:", link_idx)
    
    if durum_idx != -1 and link_idx != -1:
        for row in all_data[1:]:
            if len(row) > link_idx and len(row) > durum_idx:
                link_val = row[link_idx]
                durum_val = row[durum_idx]
                url = _extract_url(link_val)
                if url and durum_val.strip():
                    durum_map[url] = durum_val.strip()
                    
    print("durum_map:", durum_map)
    
    new_data = [["new header"]]
    for row in all_data[1:]:
        def get_val(key, default=""):
            idx = col_map.get(key, -1)
            if idx != -1 and idx < len(row): return row[idx]
            return default
        link_raw = get_val("Link")
        url = _extract_url(link_raw)
        status = ""
        if url in durum_map: status = durum_map[url]
        print(f"URL: {url}, STATUS: {status}")

simulate()
