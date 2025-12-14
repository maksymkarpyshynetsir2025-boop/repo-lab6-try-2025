import os
from csv_handler import CSVFileHandler, FileNotFound, FileCorrupted

os.makedirs("lab6", exist_ok=True)
file_path = "lab6/data.csv"

# Create the file if it does not exist
if not os.path.exists(file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("")

try:
    handler = CSVFileHandler(file_path)
except FileNotFound as e:
    print(e)
    exit()

while True:
    print("\nEnter a new name and age (or enter 'exit', to quit):")
    name = input("Name: ").strip()
    if name.lower() == "exit":
        break
    age = input("Вік: ").strip()
    if age.lower() == "exit":
        break
    if not age.isdigit():
        print("Age must be a number!")
        continue

    try:
        handler.append([[name, age]])
        print(f"{name} Successfully added!")
    except FileCorrupted as e:
        print(e)

# Read and display all data as a table
try:
    data = handler.read()
    print("\nFinal table:")
    for row in data:
        print(f"{row[0]:<10} | {row[1]}")
except FileCorrupted as e:
    print(e)
