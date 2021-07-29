import openpyxl
import sqlite3


def create_portfolio(user):
    file = openpyxl.load_workbook(f"{user}.xlsx")
    sheet = file['Сделки']

    line = sheet.max_row
    while line != 1:
        ticker = sheet.cell(row=line, column=5)
        operation = sheet.cell(row=line, column=8)
        count = sheet.cell(row=line, column=9)
        prise = sheet.cell(row=line, column=17)

        add_in_db(user, ticker.value, operation.value, count.value, float('{:.2f}'.format(prise.value)))
        line -= 1


def add_in_db(user, ticker, operation, count, prise):
    connect_db = sqlite3.connect("user_portfolio.db")
    cursor = connect_db.cursor()
    cursor.execute(f""" CREATE TABLE IF NOT EXISTS "{user}" (ticker TEXT, count INT, cost REAL) """)
    connect_db.commit()

    cursor.execute(f""" SELECT ticker FROM "{user}" WHERE ticker = "{ticker}" """)
    check = cursor.fetchone()
    if check is None:
        cursor.execute(f""" INSERT INTO "{user}" VALUES (?, ?, ?) """, (ticker, count, prise))
        connect_db.commit()
    else:
        if operation == "Покупка":
            cursor.execute(f""" SELECT * FROM "{user}" WHERE ticker = "{ticker}" """)
            old = cursor.fetchone()
            cursor.execute(f""" UPDATE "{user}" 
                                SET count = "{old[1] + count}", cost = "{old[2] + prise}" 
                                WHERE ticker = "{ticker}" """)
            connect_db.commit()
        elif operation == "Продажа":
            cursor.execute(f""" SELECT * FROM "{user}" WHERE ticker = "{ticker}" """)
            old = cursor.fetchone()
            if old[1] - count == 0:
                cursor.execute(f""" DELETE FROM "{user}" WHERE ticker = "{ticker}" """)
                connect_db.commit()
            else:
                cursor.execute(f""" UPDATE "{user}" 
                                    SET count = "{old[1] - count}", cost = "{old[2] - prise}" 
                                    WHERE ticker = "{ticker}" """)
                connect_db.commit()

    cursor.close()
    connect_db.close()
