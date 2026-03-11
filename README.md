# 💰 Expense Tracker (Python CLI)

A simple **command-line expense tracker** built with Python and **pandas** that helps you record, manage, and analyze your daily expenses.  
All data is stored locally in a **CSV file**, making it lightweight and easy to use without any database setup.

---

# ✨ Features

## ➕ Add New Expense
Record a new expense with:
- Amount
- Category
- Optional note
- Automatically recorded date

You can choose from predefined categories or create a **custom category**.

---

## 📋 View All Expenses
Displays all recorded expenses in a formatted table including:
- ID
- Date
- Amount
- Category
- Note

Also shows:
- **Grand total spending**
- **Number of records**

---

## 📅 Monthly Spending Summary
Shows statistics for a selected month:
- Spending **per category**
- **Total monthly expenses**
- **Average spending per active day**
- **Number of transactions**

---

## 🏷️ Category Analysis
Displays **all-time spending by category** with:
- Total spent
- Percentage of overall spending
- Text-based bar visualization

This helps quickly identify where most money is going.

---

## 🗑️ Delete Expense
Allows deleting a specific expense using its **ID**.  
Includes a confirmation step to prevent accidental deletion.

---

# 🗂 Data Storage

All expenses are saved in:

```
expenses.csv
```

Structure of the file:

| Column | Description |
|------|-------------|
| id | Unique expense ID |
| date | Date of transaction |
| amount | Amount spent |
| category | Expense category |
| note | Optional note |

Example:

```
id,date,amount,category,note
1,2026-03-10,12.50,Food & Dining,Lunch
2,2026-03-10,3.00,Transport,Bus fare
```

---

# 📦 Requirements

Python **3.8+**

Library:

```
pandas
```

Install dependency:

```bash
pip install pandas
```

---

# ▶️ How to Run

Run the script from your terminal:

```bash
python expense_tracker.py
```

The program will automatically create `expenses.csv` if it does not exist.

---

# 📋 Main Menu

When running the program, you will see:

```
1. Add a new expense
2. View all expenses
3. View monthly totals
4. View spending by category
5. Delete an expense
6. Quit
```

Simply enter the number of the action you want to perform.

---

# ⚙️ How It Works

The program uses **pandas DataFrames** to manage expense data.

Basic workflow:

1. Load existing expenses from the CSV file
2. Perform operations (add, view, analyze, delete)
3. Save updates back to the CSV file

This approach keeps the program simple while still enabling useful data analysis.

---

# 📊 Example Output

Example category summary:

```
Category                 Total     %   Bar
------------------------------------------------
Food & Dining           $120.50  45%  ███████████
Transport               $60.00   22%  ██████
Entertainment           $45.00   17%  ████
Shopping                $40.00   16%  ███
------------------------------------------------
TOTAL                  $265.50  100%
```
