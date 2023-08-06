from pathlib import Path
import xlwings as xw
import pandas as pd


def get_highlighted_rows(workbook1: str, workbook2: str, ws_name: str, start_row: int = 2):
    """ return a list of workbook2 row numbers that have different contents to workbook1
    Parameters:
    workbook1(str): initial excel workbook
    workbook2(str): updated excel workbook
    ws_name(str): worksheet name in the workbook to compare
    start_row(int): start data row with default = 2

    return adj_highlight_rows(list of int): list of row numbers that have different contents
    """
    if not ws_name in pd.ExcelFile(workbook1).sheet_names or not ws_name in pd.ExcelFile(workbook2).sheet_names:
        raise ValueError(f"Worksheet named '{ws_name}' not found.")

    df_initial = pd.read_excel(workbook1, ws_name)
    df_update = pd.read_excel(workbook2, ws_name)
    df_update = df_update.reset_index()
    df_diff = pd.merge(df_initial, df_update, how='outer', indicator="Exist")
    df_highlight = df_diff.query("Exist == 'right_only'")
    highlight_rows = df_highlight['index'].tolist()
    adj_highlight_rows = [start_row + int(row) for row in highlight_rows]
    return adj_highlight_rows


def highlight_diff_rows(workbook1: str, workbook2: str, ws_name: str, start_row: int = 2, output_filename: str = "SHEET_compare_rows.xlsx"):
    """ return a new workbook with different rows highlighted on workbook2
    Parameters:
    workbook1(str): initial excel workbook
    workbook2(str): updated excel workbook
    ws_name(str): the worksheet name that need to compare
    start_row(int): start data row with default = 2
    output_filename(str): the new workbook name with default name = "BOOK_compare.xlsx"

    return a new workbook with name as per default name or output_filename
    """
    # ONLY PROCESS .XLSX
    # ONLY PROCESS .XLSX
    if not workbook1.endswith('.xlsx') or not workbook2.endswith('.xlsx'):
        print("The input file to compare is not excel file")
        return

    with xw.App(visible=False) as app:
        updated_wb = app.books.open(workbook2)
        updated_ws = updated_wb.sheets(ws_name)
        highlight_rows = get_highlighted_rows(workbook1, workbook2, ws_name, start_row) \

        rng = updated_ws.used_range
        for row in rng.rows:
            if row.row in highlight_rows:
                row.color = (255, 125, 125)
        updated_wb.save(output_filename)


def highlight_diff_cells_comments(workbook1: str, workbook2: str, ws_name: str, output_filename: str = "SHEET_compare_cells.xlsx"):
    """ Slow process - Compare worksheet and highlighted the rows that have different value.

    parameters:
    workbook1 (str): the initial workbook name
    workbook2 (str): the updated workbook name to compare
    ws_name (str): the worksheet name that need to compare
    output_filename (str): the output workbook filename

    return new workbook, that sheet where the cell have different value with the initial sheet are highlighted.
    """
    if not workbook1.endswith('.xlsx') or not workbook2.endswith('.xlsx'):  # ONLY PROCESS .XLSX
        print("The input file to compare is not excel file")
        return

    with xw.App(visible=False) as app:
        initial_wb = app.books.open(workbook1)
        initial_ws = initial_wb.sheets(ws_name)  # VAR
        updated_wb = app.books.open(workbook2)
        updated_ws = updated_wb.sheets(ws_name)  # VAR
        for cell in updated_ws.used_range:
            old_value = initial_ws.range(cell.row, cell.column).value
            if cell.value != old_value:
                cell.api.AddComment(
                    f"Value from {initial_wb.name}: {old_value}")
                cell.color = (255, 30, 30)  # red color

        updated_wb.save(output_filename)
