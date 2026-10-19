import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# 1. File banayein agar pehle se nahi hai
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Type"]) # Type: Income/Expense

# 2. Naya Entry Add Karne ka Function
def add_entry():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    
    category = input("Enter category (e.g., Food, Salary, Rent): ")
    amount = float(input("Enter amount: "))
    entry_type = input("Is this Income or Expense? (I/E): ").upper()
    
    type_str = "Income" if entry_type == 'I' else "Expense"
    
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, type_str])
    print("✅ Entry added successfully!")

# 3. Monthly Summary Dekhne ka Function
def show_summary():
    month = input("Enter month to view summary (YYYY-MM): ")
    
    df = pd.read_csv(FILE_NAME)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    month_data = df[df['Month'] == month]
    
    if month_data.empty:
        print("❌ No records found for this month.")
        return
    
    income = month_data[month_data['Type'] == 'Income']['Amount'].sum()
    expense = month_data[month_data['Type'] == 'Expense']['Amount'].sum()
    balance = income - expense
    
    print(f"\n--- Summary for {month} ---")
    print(f"Total Income: {income}")
    print(f"Total Expense: {expense}")
    print(f"Net Balance: {balance}")
    print("----------------------------\n")

# 4. Chart / Graph Export Karne ka Function
def export_chart():
    df = pd.read_csv(FILE_NAME)
    expenses = df[df['Type'] == 'Expense']
    
    if expenses.empty:
        print("❌ No expenses to plot.")
        return
        
    category_sum = expenses.groupby('Category')['Amount'].sum()
    
    plt.figure(figsize=(8, 5))
    category_sum.plot(kind='bar', color='salmon')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    plt.savefig("expense_chart.png")
    print("✅ Chart saved as 'expense_chart.png' in your folder!")

# 5. Main Menu (CLI)
def main():
    initialize_file()
    while True:
        print("\n=== Expense Tracker CLI ===")
        print("1. Add Income/Expense")
        print("2. View Monthly Summary")
        print("3. Export Chart (Image)")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ")
        
        if choice == '1':
            add_entry()
        elif choice == '2':
            show_summary()
        elif choice == '3':
            export_chart()
        elif choice == '4':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()