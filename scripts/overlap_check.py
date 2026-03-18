import pandas as pd
import re

def parse_hyperlink(val):
    if pd.isna(val): return ""
    val = str(val).strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', val, re.IGNORECASE)
    if m: return m.group(1)
    return val

def analyze_overlap():
    print("Reading Excel files...")
    df_old = pd.read_excel("Job Radar - Old.xlsx")
    df_new = pd.read_excel("Job Radar - New.xlsx")
    
    old_urls = set()
    old_tcs = set()
    
    for _, row in df_old.iterrows():
        url = parse_hyperlink(row.get("Link", ""))
        url = url.split("?")[0] if url else ""
        t = str(row.get("Başlık", "")).strip().lower()
        c = str(row.get("Firma", "")).strip().lower()
        
        if url: old_urls.add(url)
        if t and c: old_tcs.add(f"{t}|{c}")
        
    new_in_old = 0
    brand_new = []
    
    for _, row in df_new.iterrows():
        url = parse_hyperlink(row.get("Link", ""))
        url = url.split("?")[0] if url else ""
        t = str(row.get("Başlık", "")).strip().lower()
        c = str(row.get("Firma", "")).strip().lower()
        
        if url in old_urls or f"{t}|{c}" in old_tcs:
            new_in_old += 1
        else:
            brand_new.append(f"{t} | {c}")
            
    print(f"\nStats:")
    print(f"Old Sheet Total: {len(df_old)}")
    print(f"New Sheet Total: {len(df_new)}")
    print(f"Jobs in NEW that were already in OLD: {new_in_old}")
    print(f"Brand completely NEW jobs: {len(brand_new)}")
    
    if len(brand_new) > 0:
        print("\nFirst 10 truly new jobs:")
        for job in brand_new[:10]:
            print(f"- {job}")

if __name__ == "__main__":
    analyze_overlap()
