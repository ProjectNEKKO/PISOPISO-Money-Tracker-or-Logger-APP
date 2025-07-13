import csv
import os

def load_transactions(filename):
  transactions = []
  if not os.path.exists(filename):
    return transactions

  with open(filename, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
      transactions.append(row)

  return transactions

def save_transaction(filename, txn):
  file_exists = os.path.exists(filename)

  with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "description"])

    if not file_exists:
      writer.writeheader()

    writer.writerow(txn)