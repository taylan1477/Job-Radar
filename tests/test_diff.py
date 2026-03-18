def simulate():
    old = [
        ["Baslik", "Firma", "Link", "Durum"],
        ["Soft Eng", "Google", "http://a", "Favori"], # In new
        ["Soft Eng", "", "http://b", "Reddedildi"],    # Not in new, empty company
        ["Soft Eng", "Apple", "http://c", "Basvuruldu"] # Not in new
    ]
    new = [
        ["Baslik", "Firma", "Link", "Durum"],
        ["Soft Eng", "Google", "http://a", ""]
    ]
    
    new_urls = set(["http://a"])
    new_tcs = set(["soft eng|google", "soft eng|"])

    rows_to_append = []
    
    for row in old[1:]:
        t = row[0].strip().lower()
        c = row[1].strip().lower()
        url = row[2]
        tc_key = f"{t}|{c}"
        
        exists_in_new = False
        if url and url in new_urls: 
            exists_in_new = True
        elif tc_key and t and c and tc_key in new_tcs: 
            exists_in_new = True
            
        if not exists_in_new:
            rows_to_append.append(row)
            
    print("To append:", rows_to_append)

simulate()
