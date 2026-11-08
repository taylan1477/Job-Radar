import os
import re
import urllib.request
import ssl

BASE_DIR = r"c:\Projeler\PycharmProjects\job-radar\cv_suite\Humanized_CV"
PDF_DIR = os.path.join(BASE_DIR, "pdf")
MD_DIR = os.path.join(BASE_DIR, "markdown")
HTML_DIR = os.path.join(BASE_DIR, "html")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("======================================================================")
print("🔍 STAGE 3 QA AUDIT: LAYOUT, PDF PAGES, HYPERLINKS & UNICODE INTEGRITY")
print("======================================================================")

# 1. Page Count Audit
print("\n--- 1. PDF Page Budget & Single Page Check ---")
pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
page_audit_passed = True
for pdf in sorted(pdf_files):
    pdf_path = os.path.join(PDF_DIR, pdf)
    with open(pdf_path, "rb") as f:
        data = f.read()
    pages = len(re.findall(rb'/Type\s*/Page\b', data))
    size_kb = os.path.getsize(pdf_path) / 1024
    status = "PASS (1 Page)" if pages == 1 else f"FAIL ({pages} Pages)"
    if pages != 1:
        page_audit_passed = False
    print(f"  [{status}] {pdf} ({size_kb:.1f} KB)")

# 2. Hyperlink Verification
print("\n--- 2. Hyperlink Accessibility & HTTP Status Check ---")
unique_urls = set()
for md in os.listdir(MD_DIR):
    if md.endswith(".md"):
        with open(os.path.join(MD_DIR, md), "r", encoding="utf-8") as f:
            content = f.read()
            urls = re.findall(r'https?://[^\s\)]+', content)
            for u in urls:
                # clean trailing brackets or punctuation
                clean_u = u.rstrip('.,;)]>')
                unique_urls.add(clean_u)

link_audit_passed = True
for url in sorted(unique_urls):
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"}
        )
        with urllib.request.urlopen(req, timeout=8, context=ctx) as response:
            status = response.getcode()
            print(f"  [HTTP {status}] {url}")
    except urllib.error.HTTPError as e:
        # LinkedIn might return 999 or 403 to automated bots
        if "linkedin.com" in url and e.code in [999, 403]:
            print(f"  [OK / Bot-Protected: HTTP {e.code}] {url} (Valid Profile URL)")
        else:
            print(f"  [WARN HTTP {e.code}] {url}")
            link_audit_passed = False
    except Exception as e:
        print(f"  [ERR: {e}] {url}")
        link_audit_passed = False

# 3. Unicode & Turkish Character Integrity
print("\n--- 3. Unicode & Turkish Character Integrity ---")
turkish_chars = ["ğ", "ü", "ş", "ı", "ö", "ç", "İ", "Ğ", "Ü", "Ş", "Ö", "Ç"]
unicode_passed = True
for tr_md in [f for f in os.listdir(MD_DIR) if "_TR" in f]:
    with open(os.path.join(MD_DIR, tr_md), "r", encoding="utf-8") as f:
        text = f.read()
    found_chars = {c: text.count(c) for c in turkish_chars if text.count(c) > 0}
    # Check for corruption markers
    has_corruption = any(bad in text for bad in ["\ufffd", "Ã¼", "ÅŸ", "ÄŸ", "Ä±", "Ã¶", "Ã§"])
    if has_corruption:
        unicode_passed = False
        print(f"  [FAIL] {tr_md} contains mojibake/corrupted characters!")
    else:
        sample = ", ".join([f"{k}:{v}" for k, v in list(found_chars.items())[:6]])
        print(f"  [PASS UTF-8] {tr_md} -> Valid characters verified ({sample})")

print("\n======================================================================")
print(f"STAGE 3 SUMMARY: Pages: {'PASS' if page_audit_passed else 'FAIL'} | Links: {'PASS' if link_audit_passed else 'FAIL'} | Unicode: {'PASS' if unicode_passed else 'FAIL'}")
print("======================================================================")
