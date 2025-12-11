import os
from csv_handler import CSVFileHandler, FileNotFound, FileCorrupted

os.makedirs("lab6", exist_ok=True)
file_path = "lab6/data.csv"

# Створюємо файл, якщо його немає
if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("")

try:
    handler = CSVFileHandler(file_path)
except FileNotFound as e:
    print(e)
    exit()

while True:
    print("\nВведи нове ім'я та вік (або введи 'exit', щоб завершити):")
    name = input("Ім'я: ").strip()
    if name.lower() == "exit":
        break
    age = input("Вік: ").strip()
    if age.lower() == "exit":
        break
    if not age.isdigit():
        print("Вік має бути числом!")
        continue

    try:
        handler.append([[name, age]])
        print(f"{name} додано успішно!")
    except FileCorrupted as e:
        print(e)

# Зчитуємо і показуємо всі дані як таблицю
try:
    data = handler.read()
    print("\nФінальна таблиця:")
    for row in data:
        print(f"{row[0]:<10} | {row[1]}")
except FileCorrupted as e:
    print(e)
