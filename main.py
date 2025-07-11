import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import (
  QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QDateEdit,
  QComboBox, QLineEdit, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PySide6.QtCore import QDate

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("PisoPiso")
    self.resize(500, 400)

    self.central = QWidget()
    self.setCentralWidget(self.central)
    self.main_layout = QVBoxLayout()
    self.central.setLayout(self.main_layout)
    self.transaction = []

    self.build_input_group()
    self.build_transaction_table()

  def build_input_group(self):
    group = QGroupBox("Add New Transaction")
    form_layout = QFormLayout()

    self.date_input = QDateEdit()
    self.date_input.setDate(QDate.currentDate())

    self.type_input = QComboBox()
    self.type_input.addItems(["Income","Expense"])

    self.category_input = QComboBox()
    self.category_input.addItems(["Salary","Food", "Bills", "Transport", "Other"])

    self.amount_input = QLineEdit()
    self.amount_input.setPlaceholderText("Enter amount")

    self.desc_input = QLineEdit()
    self.desc_input.setPlaceholderText("Optional")

    self.add_button = QPushButton("+ Add Transaction")
    self.add_button.clicked.connect(self.handle_add)

    form_layout.addRow("Date: ", self.date_input)
    form_layout.addRow("Type: ", self.type_input)
    form_layout.addRow("Category", self.category_input)
    form_layout.addRow("Amount (₱)", self.amount_input)
    form_layout.addRow("Description:", self.desc_input)
    form_layout.addRow("", self.add_button)

    group.setLayout(form_layout)
    self.main_layout.addWidget(group)

  def handle_add(self):
    date = self.date_input.date().toString("yyyy-MM-dd")
    type_ = self.type_input.currentText()
    category = self.category_input.currentText()
    amount = self.amount_input.text()
    description = self.desc_input.text()

    transaction = {
      "date": date,
      "type": type_,
      "category": category,
      "amount": amount,
      "description": description,
    }

    self.transaction.append(transaction)
    self.update_table()

    print(f"✅ Added: {transaction}")
    print(f"📊 Total transaction: {len(self.transaction)}")

  def build_transaction_table(self):
    self.table = QTableWidget()
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Amount (₱)", "Description"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.main_layout.addWidget(self.table)

  def update_table(self):
    self.table.setRowCount(len(self.transaction))

    for row, txn in enumerate(self.transaction):
      self.table.setItem(row, 0, QTableWidgetItem(txn["date"]))
      self.table.setItem(row, 1, QTableWidgetItem(txn["type"]))
      self.table.setItem(row, 2, QTableWidgetItem(txn["category"]))
      self.table.setItem(row, 3, QTableWidgetItem(txn["amount"]))
      self.table.setItem(row, 4, QTableWidgetItem(txn["description"]))

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())