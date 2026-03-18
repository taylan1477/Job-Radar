import pandas as pd
import re

def parse_hyperlink(val):
    if pd.isna(val): return ""
    val = str(val).strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', val, re.IGNORECASE)
    if m: return m.group(1)
    return val

def analyze():
    print("Reading Excel files...")
    df_old = pd.read_excel("Job Radar - Old.xlsx")
    df_new = pd.read_excel("Job Radar - New.xlsx")
    df_merged = pd.read_excel("Job Radar - Merged.xlsx")
    
    # We just need to check if there are status values in "Durum" column in OLD
    # that are not in MERGED
    
    print(f"Old length: {len(df_old)}")
    print(f"New length: {len(df_new)}")
    print(f"Merged length: {len(df_merged)}")
    
    if "Durum" in df_old.columns:
        old_with_status = df_old[df_old["Durum"].notna() & (df_old["Durum"] != "")]
        print(f"Old has {len(old_with_status)} rows with Durum")
        
        # Check what happened to these in MERGED
        merged_urls = set()
        if "Link" in df_merged.columns:
            for url in df_merged["Link"]:
                merged_urls.add(parse_hyperlink(url))
                
        merged_tcs = set()
        if "Başlık" in df_merged.columns and "Firma" in df_merged.columns:
            for _, row in df_merged.iterrows():
                t = str(row["Başlık"]).strip().lower()
                c = str(row["Firma"]).strip().lower()
                merged_tcs.add(f"{t}|{c}")
                
        missing = []
        for _, row in old_with_status.iterrows():
            url = parse_hyperlink(row.get("Link", ""))
            t = str(row.get("Başlık", "")).strip().lower()
            c = str(row.get("Firma", "")).strip().lower()
            
            base_url = url.split("?")[0] if url else ""
            tc_key = f"{t}|{c}"
            
            found = False
            if url and url in merged_urls: found = True
            elif base_url and base_url in merged_urls: found = True
            elif tc_key and t and c and tc_key in merged_tcs: found = True
            
            if not found:
                missing.append((t, c, url, row["Durum"]))
                
        print(f"\nMissing {len(missing)} rows in Merged:")
        for t, c, url, status in missing[:5]:
            print(f"- {t} | {c} | {status} | {url[:40]}...")
            
    else:
        print("No Durum column in Old")

if __name__ == "__main__":
    analyze()
