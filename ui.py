from PySide6.QtWidgets import (
  QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
  QLabel, QLineEdit, QComboBox, QPushButton, QDateEdit,
  QTableWidget, QTableWidgetItem, QHeaderView, QGroupBox, QFormLayout,
  QMessageBox, QFileDialog
)
from PySide6.QtCore import (QDate, Qt)
from PySide6.QtGui import QDoubleValidator

from data import load_transactions, save_transaction
from app_state import AppState

import csv

class PisoPisoApp(QMainWindow):
  def __init__(self, state: AppState):
    super().__init__()

    self.editing_index = None

    self.state = state
    self.setWindowTitle("PisoPiso")
    self.setMinimumSize(600, 500)

    self.main_widget = QWidget()
    self.setCentralWidget(self.main_widget)

    self.main_layout = QVBoxLayout()
    self.main_widget.setLayout(self.main_layout)

    self.main_layout.setContentsMargins(15, 15, 15, 15)
    self.main_layout.setSpacing(12)

    self.build_input_group()
    self.build_transaction_table()

    self.export_button = QPushButton("⏬ Export CSV")
    self.export_button.clicked.connect(self.export_to_csv)


    self.remove_button = QPushButton("🗑️ Remove")
    self.remove_button.clicked.connect(self.remove_selected_transaction)


    self.clear_button = QPushButton("🧼 Clear All")
    self.clear_button.clicked.connect(self.clear_all_transaction)


    self.edit_button = QPushButton("✏️ Edit")
    self.edit_button.clicked.connect(self.edit_selected_transaction)

    button_layout = QHBoxLayout()
    button_layout.setSpacing(10)

    button_layout.addWidget(self.export_button)
    button_layout.addWidget(self.remove_button)
    button_layout.addWidget(self.clear_button)
    button_layout.addWidget(self.edit_button)

    self.main_layout.addLayout(button_layout)

    self.build_summary_labels()

    self.state.transactions = load_transactions(self.state.csv_file)
    self.update_table()
    self.update_summary()



  def build_input_group(self):
    group = QGroupBox("Add New Transaction")
    form_layout = QFormLayout()

    self.date_input = QDateEdit()
    self.date_input.setDate(QDate.currentDate())
    self.date_input.setCalendarPopup(True)

    self.type_input = QComboBox()
    self.type_input.addItems(["Income", "Expense"])

    self.category_input = QComboBox()
    self.category_input.addItems(["Salary", "Food", "Bills", "Transport", "Other"])

    self.amount_input = QLineEdit()
    self.amount_input.setValidator(QDoubleValidator(0.00, 9999999.99, 2))
    self.amount_input.setPlaceholderText("Enter amount")

    self.desc_input = QLineEdit()
    self.desc_input.setPlaceholderText("Optional")

    self.add_button = QPushButton("+ Add Transaction")
    self.add_button.clicked.connect(self.handle_add)

    type_layout = QHBoxLayout()
    type_label = QLabel("Type:")
    type_label.setFixedWidth(63)
    type_layout.addWidget(type_label)
    type_layout.addWidget(self.type_input)

    category_layout = QHBoxLayout()
    category_label = QLabel("Category:")
    category_label.setFixedWidth(60)
    category_layout.addWidget(category_label)
    category_layout.addWidget(self.category_input)

    type_cat_layout = QHBoxLayout()
    type_cat_layout.addLayout(type_layout)
    type_cat_layout.addSpacing(20)
    type_cat_layout.addLayout(category_layout)

    form_layout.addRow(type_cat_layout)

    self.date_input.setFixedWidth(130)
    self.amount_input.setFixedWidth(150)
    self.desc_input.setMinimumWidth(200)

    row1 = QHBoxLayout()

    date_label = QLabel("Date:")
    date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    row1.addWidget(date_label)
    row1.addWidget(self.date_input)

    row1.addSpacing(10)

    amount_label = QLabel("Amount:")
    amount_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    row1.addWidget(amount_label)
    row1.addWidget(self.amount_input)

    row1.addSpacing(10)

    desc_label = QLabel("Description:")
    desc_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    row1.addWidget(desc_label)
    row1.addWidget(self.desc_input)

    form_layout.addRow(row1)
    form_layout.addRow("", self.add_button)

    group.setLayout(form_layout)
    self.main_layout.addWidget(group)



  def build_transaction_table(self):
    self.table = QTableWidget()
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels(["Date", "Type", "Category", "Amount (₱)", "Description"])
    self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    self.table.setEditTriggers(QTableWidget.NoEditTriggers)
    self.main_layout.addWidget(self.table)



  def build_summary_labels(self):
    self.income_label = QLabel("Total Income: ₱0.00")
    self.expense_label = QLabel("Total Expense: ₱0.00")
    self.balance_label = QLabel("Balance: ₱0.00")

    font = self.income_label.font()
    font.setPointSize(10)
    font.setBold(True)

    self.income_label.setFont(font)
    self.expense_label.setFont(font)
    self.balance_label.setFont(font)

    summary_layout = QHBoxLayout()
    summary_layout.setSpacing(30)

    summary_layout.addStretch()
    summary_layout.addWidget(self.income_label)
    summary_layout.addWidget(self.expense_label)
    summary_layout.addWidget(self.balance_label)

    self.main_layout.addLayout(summary_layout)
    


  def handle_add(self):
    amount_text = self.amount_input.text().strip()

    if not amount_text:
      QMessageBox.warning(self, "Missing Amount", "Please enter a valid amount.")
      return
    
    try:
      amount = float(amount_text)
      if amount <= 0:
        raise ValueError
    except ValueError:
      QMessageBox.warning(self, "Invalid Amount", "Amount must be a positive number.")
      return

    transaction = {
      "date": self.date_input.date().toString("yyyy-MM-dd"),
      "type": self.type_input.currentText(),
      "category": self.category_input.currentText(),
      "amount": self.amount_input.text(),
      "description": self.desc_input.text()
    }

    if self.editing_index is not None:
      self.state.transactions[self.editing_index] = transaction
      self.editing_index = None
      self.add_button.setText("+ Add Transaction")
    else:
      self.state.transactions.append(transaction)

    try:
      with open(self.state.csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = ["date", "type", "category", "amount", "description"])
        writer.writeheader()
        for txn in self.state.transactions:
          writer.writerow(txn)
    except Exception as e:
      QMessageBox.critical(self, "Error", f"Failed to update CSV:\n{e}")
      return

    self.update_table()
    self.update_summary()

    self.amount_input.clear()
    self.desc_input.clear()



  def export_to_csv(self):
    if not self.state.transactions:
      QMessageBox.information(self, "No Data", "There are no transactions to export.")
      return
    
    file_path, _ = QFileDialog.getSaveFileName(
      self,
      "Export Transaction"
      "Transactions.csv"
      "CSV Files (*csv)"
    )

    if not file_path:
      return
    
    if not file_path.lower().endswith(".csv"):
      file_path += ".csv"
    
    try:
      with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames = ["date", "type", "category", "amount", "description"])
        writer.writeheader()
        for txn in self.state.transactions:
          writer.writerow(txn)

      QMessageBox.information(self, "Export Succesful", f"Transactions saved to:\n{file_path}")

    except Exception as e:
      QMessageBox.critical(self, "Export Failed", f"An error occured:\n{e}")



  def remove_selected_transaction(self):
    selected = self.table.currentRow()

    if selected == -1:
      QMessageBox.information(self, "No Selection", "Please select a transaction to remove.")
      return
  
    confirm = QMessageBox.question(
      self,
      "Confirm Deletion",
      "Are you sure you want to delete this transaction?",
      QMessageBox.Yes | QMessageBox.No 
    )

    if confirm != QMessageBox.Yes:
      return
    
    del self.state.transactions[selected]

    try:
      with open(self.state.csv_file, mode = 'w', newline = '', encoding = 'utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "description"])
        writer.writeheader()
        for txn in self.state.transactions:
          writer.writerow(txn)
    except Exception as e:
      QMessageBox.critical(self, "Error", f"Failed to update CSV:\n{e}")
      return
    
    self.update_table()
    self.update_summary()



  def edit_selected_transaction(self):
    row = self.table.currentRow()
    if row == -1:
      QMessageBox.information(self, "No Selection", "Please select a transaction to edit.")
      return
    
    txn = self.state.transactions[row]
    self.editing_index = row

    self.date_input.setDate(QDate.fromString(txn["date"], "yyyy-MM-dd"))
    self.type_input.setCurrentText(txn["type"])
    if isinstance(self.category_input, QComboBox):
      self.category_input.setCurrentText(txn["category"])
    else:
      self.category_input.setText(txn["category"])
    self.amount_input.setText(txn["amount"])
    self.desc_input.setText(txn["description"])

    self.add_button.setText("✅ Update Transaction")




  def clear_all_transaction(self):
    if not self.state.transactions:
      QMessageBox.information(self, "Nothing to clear", "There are no transactions to clear.")
      return
    
    confirm = QMessageBox.question(
      self,
      "Confirm Clear All",
      "Are you sure you want to delete ALL transactions?",
      QMessageBox.Yes | QMessageBox.No
    )

    if confirm != QMessageBox.Yes:
      return
    
    self.state.transactions.clear()

    try:
      with open(self.state.csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["date", "type", "category", "amount", "description"])
        writer.writeheader()
    except Exception as e:
      QMessageBox.critical(self, "Error", f"Failed to clear CSV\n{e}")
      return
    
    self.update_table()
    self.update_summary()


  def update_table(self):
    self.table.setRowCount(len(self.state.transactions))
    for row, txn in enumerate(self.state.transactions):
      self.table.setItem(row, 0, QTableWidgetItem(txn["date"]))
      self.table.setItem(row, 1, QTableWidgetItem(txn["type"]))
      self.table.setItem(row, 2, QTableWidgetItem(txn["category"]))
      self.table.setItem(row, 3, QTableWidgetItem(txn["amount"]))
      self.table.setItem(row, 4, QTableWidgetItem(txn["description"]))



  def update_summary(self):
    income_total = 0
    expense_total = 0

    for txn in self.state.transactions:
      try:
        amt = float(txn["amount"])
      except ValueError:
        amt = 0

      if txn["type"] == "Income":
        income_total += amt
      else:
        expense_total += amt

    balance = income_total - expense_total

    self.income_label.setText(f"Total Income: ₱{income_total:,.2f}")
    self.expense_label.setText(f"Total Expense: ₱{expense_total:,.2f}")
    self.balance_label.setText(f"Balance: ₱{balance:,.2f}")

    if balance < 0:
      self.balance_label.setStyleSheet("color: red; font-weight: bold;")
    elif balance == 0:
      self.balance_label.setStyleSheet("color: gray; font-weight: bold;")
    else:
      self.balance_label.setStyleSheet("color: green; font-weight: bold;")