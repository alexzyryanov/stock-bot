import openpyxl


file = openpyxl.load_workbook("1.xlsx")
sheet = file['Сделки']
print(sheet.max_row)

all_item = {}
line = sheet.max_row
while line != 1:
    print(line)
    ticker = sheet.cell(row=line, column=5)
    prise = sheet.cell(row=line, column=17)
    sell_buy = sheet.cell(row=line, column=8)
    print(ticker.value, prise.value, sell_buy.value)
    if ticker.value in all_item:
        if sell_buy.value == "Покупка":
            all_item[ticker.value] += float('{:.2f}'.format(prise.value))
        elif sell_buy.value == "Продажа":
            all_item[ticker.value] -= float('{:.2f}'.format(prise.value))
    else:
        all_item.update({ticker.value: float('{:.2f}'.format(prise.value))})

    line -= 1

# print(all_item)
for t, c in all_item.items():
    print(t, float('{:.2f}'.format(c)))
