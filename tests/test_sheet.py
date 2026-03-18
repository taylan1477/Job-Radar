import sys
from src.clients.sheets_client import _get_sheet, _extract_url

def main():
    ws = _get_sheet()
    if not ws:
        print("Failed to get sheet")
        return
        
    data = ws.get_all_values(value_render_option="FORMULA")
    # FORMULA modu sayilari float yapabilir, str'ye cevir
    all_data = [[str(cell) if not isinstance(cell, str) else cell for cell in row] for row in data]

    print("Header len:", len(data[0]))
    print("Header:", data[0])
    
    if len(all_data) > 1:
        row = all_data[1]
        print(f"Row 1 len: {len(row)}")
        print(f"Row 1: {row}")
        if len(row) > 6:
            url = _extract_url(row[6])
            print(f"URL extraction index 6: {url}")
        else:
            print("Row doesn't have 7 columns")

if __name__ == "__main__":
    main()
