import re
def _extract_url(cell_value):
    if not cell_value: return ""
    cell_value = str(cell_value).strip()
    m = re.match(r'=HYPERLINK\("([^"]+)"[;,]', cell_value, re.IGNORECASE)
    if m: return m.group(1)
    return cell_value

def debug():
    # Simulate what's happening
    # Let's say user has old data with 35 status items.
    # Are they somehow matching `tc_key` with other items in the new sheet?
    # Yes, if title and company are empty, or if there's a generic title like "software engineer"
    # and no company. Let's look at the mapping logic in merge_sheets.py 
    pass
