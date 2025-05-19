from typing import List
def get_names(sheet, spreadsheet_id, sheet_id):
    ranges = [
        f"{sheet_id}!C:C",
        f"{sheet_id}!D:D"
    ]
    CD_collumn = sheet.values().batchGet(
        spreadsheetId=spreadsheet_id,
        ranges=ranges
        ).execute()
    values = CD_collumn.get('valueRanges', [])
    return values[0]["values"], values[1]["values"]
def is_broken(C_collumn, D_collumn):
    if(len(C_collumn) != len(D_collumn)):
        return True
    return False
def update_name(sheet, spreadsheet_id, sheet_id, person: List):
    lastnames, firstnames = get_names(sheet, spreadsheet_id, sheet_id)
    data = [
        {"range": f"{sheet_id}!C{len(lastnames)+1}", "values": [person[:2]]},
        #the goddamm person[2] is now a int, so it has to wrap inside a list
        {"range": f"{sheet_id}!H{len(lastnames)+1}", "values": [[person[2]]]},
        {"range": f"{sheet_id}!K{len(lastnames)+1}", "values": [person[3:]]},

    ]
    body = {"valueInputOption": "USER_ENTERED", "data":data}
    if is_broken(lastnames, firstnames): return False
    result = sheet.values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body=body,
    ).execute()
    print(f"{result.get('totalUpdatedCells')} cells updated.")
    return True
