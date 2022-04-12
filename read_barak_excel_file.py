import xlrd

def read_excel_hiyuv_file():
    loc = ("C:\\Users\\Eldad\\documents\\hiyuvpython.xls")
    login = 1
    serv = 3
    # To open Workbook
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    login_name = {}
    # For row 0 and column 0
    for i in range(sheet.nrows):
        login_name[sheet.cell_value(i,login)] = sheet.cell_value(i,serv)
    print(login_name)
    return login_name