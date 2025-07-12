import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWidgets import (
  QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QDateEdit,
  QComboBox, QLineEdit, QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView,
  QLabel
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QDoubleValidator

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("PisoPiso")
    self.resize(600, 500)

    self.central = QWidget()
    self.setCentralWidget(self.central)

    self.main_layout = QVBoxLayout()
    self.main_layout.setContentsMargins(15,15,15, 15)
    self.main_layout.setSpacing(15)

    self.central.setLayout(self.main_layout)
    self.transactions = []

    self.build_input_group()
    self.build_transaction_table()
    self.build_summary_labels()

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
    self.amount_input.setValidator(QDoubleValidator(0.00, 9999999.99, 2))
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

    self.transactions.append(transaction)
    self.update_table()
    self.update_summary()

    print(f"✅ Added: {transaction}")
    print(f"📊 Total transaction: {len(self.transactions)}")

  def build_transaction_table(self):
    self.table = QTableWidget()
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Amount (₱)", "Description"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.main_layout.addWidget(self.table)

  def update_table(self):
    self.table.setRowCount(len(self.transactions))

    for row, txn in enumerate(self.transactions):
      self.table.setItem(row, 0, QTableWidgetItem(txn["date"]))
      self.table.setItem(row, 1, QTableWidgetItem(txn["type"]))
      self.table.setItem(row, 2, QTableWidgetItem(txn["category"]))
      self.table.setItem(row, 3, QTableWidgetItem(txn["amount"]))
      self.table.setItem(row, 4, QTableWidgetItem(txn["description"]))

  def build_summary_labels(self):
    self.income_label = QLabel("Total Income: ₱0")
    self.expense_label = QLabel("Total Expense: ₱0")
    self.balance_label = QLabel("Balance: ₱0")

    summary_layout = QHBoxLayout()
    summary_layout.addWidget(self.income_label)
    summary_layout.addWidget(self.expense_label)
    summary_layout.addWidget(self.balance_label)

    self.main_layout.addLayout(summary_layout)

  def update_summary(self):
    income_total = 0
    expense_total = 0

    for txn in self.transactions:
      try:
        amt = float(txn["amount"])
      except ValueError:
        amt = 0

      if txn["type"] == "Income":
        income_total += amt
      else:
        expense_total += amt

    balance = income_total - expense_total

    if balance < 0:
      self.balance_label.setStyleSheet(
        "color: red;"
        "font-weight: bold;"
      )
    elif  balance == 0:
      self.balance_label.setStyleSheet(
        "color: white;"
        "font-weight: bold;"
      )
    else:
      self.balance_label.setStyleSheet(
        "color: green;"
        "font-weight: bold;"
      )

    self.income_label.setText(f"Total Income: ₱{income_total:,.2f}")
    self.expense_label.setText(f"Total Expense: ₱{expense_total:,.2f}")
    self.balance_label.setText(f"Balance: ₱{balance:,.2f}")

    

if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec())