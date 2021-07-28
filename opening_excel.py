import openpyxl
import sqlite3


def create_portfolio():
    file = openpyxl.load_workbook("1.xlsx")
    sheet = file['Сделки']

    print(sheet.max_row)
    line = sheet.max_row

    while line != 1:
        print(line)
        ticker = sheet.cell(row=line, column=5)
        operation = sheet.cell(row=line, column=8)
        count = sheet.cell(row=line, column=9)
        prise = sheet.cell(row=line, column=17)

        add_in_db(ticker.value, operation.value, count.value, float('{:.2f}'.format(prise.value)))
        line -= 1


def add_in_db(ticker, operation, count, prise):
    print(ticker, operation, count, prise)
    print(type(ticker), type(operation), type(count), type(prise))
    connect_db = sqlite3.connect("user_portfolio.db")
    cursor = connect_db.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS portfolio (ticker TEXT, count INT, cost REAL) """)
    connect_db.commit()

    cursor.execute(f""" SELECT ticker FROM portfolio WHERE ticker = "{ticker}" """)
    check = cursor.fetchone()
    print(check)
    if check is None:
        cursor.execute(""" INSERT INTO portfolio VALUES (?, ?, ?) """, (ticker, count, prise))
        connect_db.commit()
    else:
        if operation == "Покупка":
            cursor.execute(f""" SELECT * FROM portfolio WHERE ticker = "{ticker}" """)
            old = cursor.fetchone()
            new = f""" UPDATE portfolio SET count = "{old[1] + count}" WHERE ticker = "{ticker}" """
            cursor.execute(new)
            connect_db.commit()
            new = f""" UPDATE portfolio SET cost = "{old[2] + prise}" WHERE ticker = "{ticker}" """
            cursor.execute(new)
            connect_db.commit()
        elif operation == "Продажа":
            cursor.execute(f""" SELECT * FROM portfolio WHERE ticker = "{ticker}" """)
            old = cursor.fetchone()
            if old[1] - count == 0:
                cursor.execute(f""" DELETE FROM portfolio WHERE ticker = "{ticker}" """)
                connect_db.commit()
            else:
                new = f""" UPDATE portfolio SET count = "{old[1] - count}" WHERE ticker = "{ticker}" """
                cursor.execute(new)
                connect_db.commit()
                new = f""" UPDATE portfolio SET cost = "{old[2] - prise}" WHERE ticker = "{ticker}" """
                cursor.execute(new)
                connect_db.commit()

    cursor.close()
    connect_db.close()


create_portfolio()
