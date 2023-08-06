import xlwings as xw
import pandas as pd
from compare_ws import get_highlighted_rows


def highlight_diff_rows(workbook1: str, workbook2: str, start_row: int = 2, output_filename: str = "BOOK_compare_rows.xlsx"):
    """ return a new workbook with different rows highlighted on workbook2
    Parameters:
    workbook1(str): initial excel workbook
    workbook2(str): updated excel workbook
    start_row(int): start data row with default = 2
    output_filename(str): the new workbook name with default name = "BOOK_compare.xlsx"

    return a new workbook with name as per default name or output_filename
    """
    if not workbook1.endswith('.xlsx') or not workbook2.endswith('.xlsx'):  # ONLY PROCESS .XLSX
        print("The input file to compare is not excel file")
        return

    sheets1 = pd.ExcelFile(workbook1).sheet_names
    sheets2 = pd.ExcelFile(workbook2).sheet_names

    with xw.App(visible=False) as app:
        updated_wb = app.books.open(workbook2)
        for ws_name in sheets2:
            updated_ws = updated_wb.sheets(ws_name)
            rng = updated_ws.used_range
            if ws_name in sheets1:
                highlight_rows = get_highlighted_rows(workbook1, workbook2, ws_name, start_row) \

            else:
                highlight_rows = [row.row for row in rng.rows]

            for row in rng.rows:
                if row.row in highlight_rows:
                    row.color = (255, 125, 125)

        updated_wb.save(output_filename)


def highlight_diff_cells_comments(workbook1: str, workbook2: str, output_filename: str = "BOOK_compare_cells.xlsx"):
    """ compare each worksheet in the workbook and highlighted the cell and add comment if it has different value with the initial workbook.

    parameters:
    workbook1 (str): the initial workbook name
    workbook2 (str): the updated workbook name to compare
    output_filename (str): the output workbook filename

    return new workbook where all the cells that have different value with the initial workbook are highlighted and commented.
    """
    sheets1 = pd.ExcelFile(workbook1).sheet_names
    sheets2 = pd.ExcelFile(workbook2).sheet_names
    # ie: ['sheet1', 'sheet2']
    compare_sheets = [sh for sh in sheets2 if sh in sheets1]
    with xw.App(visible=False) as app:
        initial_wb = app.books.open(workbook1)
        updated_wb = app.books.open(workbook2)
        for ws in compare_sheets:
            initial_ws = initial_wb.sheets(ws)  # VAR
            updated_ws = updated_wb.sheets(ws)  # VAR
            for cell in updated_ws.used_range:
                old_value = initial_ws.range(cell.row, cell.column).value
                if cell.value != old_value:
                    cell.api.AddComment(
                        f"Value from {initial_wb.name}: {old_value}")
                    cell.color = (255, 30, 30)  # red color

        updated_wb.save(output_filename)
