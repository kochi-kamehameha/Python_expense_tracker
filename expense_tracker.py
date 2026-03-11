import os
import sys
from datetime import datetime

import pandas as pd

CSV_FILE = "expenses.csv"
COL_ID, COL_DATE, COL_AMOUNT, COL_CATEGORY, COL_NOTE = "id", "date", "amount", "category", "note"

CATEGORIES = [
    "Food & Dining", "Transport", "Housing & Utilities", "Health & Fitness",
    "Entertainment", "Shopping", "Education", "Travel", "Savings & Investments", "Other"
]

WIDTH = 60

def hr(char="─"):
    print(char * WIDTH)

def banner():
    print("\n" + "═" * WIDTH)
    print("  💰  EXPENSE TRACKER  —  Your Personal Finance Log")
    print("═" * WIDTH)

def menu():
    print("\n" + "─" * WIDTH)
    print("  MAIN MENU")
    print("─" * WIDTH)
    print("  1.  ➕  Add a new expense")
    print("  2.  📋  View all expenses")
    print("  3.  📅  View monthly totals")
    print("  4.  🏷️   View spending by category")
    print("  5.  🗑️   Delete an expense")
    print("  6.  🚪  Quit")
    print("─" * WIDTH)

def load_expenses() -> pd.DataFrame:
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=[COL_ID, COL_DATE, COL_AMOUNT, COL_CATEGORY, COL_NOTE])
    df = pd.read_csv(CSV_FILE)
    df[COL_DATE] = pd.to_datetime(df[COL_DATE])
    return df

def save_expenses(df: pd.DataFrame) -> None:
    out = df.copy()
    out[COL_DATE] = pd.to_datetime(out[COL_DATE]).dt.strftime("%Y-%m-%d")
    out.to_csv(CSV_FILE, index=False)

def next_id(df: pd.DataFrame) -> int:
    return int(df[COL_ID].max() + 1) if not df.empty else 1

def prompt_amount() -> float:
    while True:
        raw = input("  💵  Amount ($): ").strip()
        try:
            value = float(raw)
            if value > 0:
                return round(value, 2)
            raise ValueError
        except ValueError:
            print("  ⚠️  Enter a positive number (e.g. 12.50).")

def prompt_category() -> str:
    print("\n  Select a category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i:>2}.  {cat}")
    print(f"    {len(CATEGORIES)+1:>2}.  ✏️  Custom category")

    while True:
        choice = input(f"\n  Choice (1–{len(CATEGORIES)+1}): ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]
            if choice == len(CATEGORIES) + 1:
                custom = input("  Custom category: ").strip()
                return custom or "Other"
        print(f"  ⚠️  Enter a number 1 to {len(CATEGORIES)+1}.")

def prompt_note() -> str:
    return input("  📝  Note (optional): ").strip()

def prompt_month_year() -> tuple[int, int]:
    now = datetime.now()
    raw = input(f"  📅  Month/Year (MM/YYYY) — press Enter for {now.strftime('%m/%Y')}: ").strip()
    if not raw:
        return now.month, now.year
    try:
        dt = datetime.strptime(raw, "%m/%Y")
        return dt.month, dt.year
    except ValueError:
        print(f"  ⚠️  Invalid format, using current month.")
        return now.month, now.year

def add_expense(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "─" * WIDTH)
    print("  ➕  ADD NEW EXPENSE")
    print("─" * WIDTH)

    amount = prompt_amount()
    category = prompt_category()
    note = prompt_note()
    today = datetime.now().strftime("%Y-%m-%d")
    exp_id = next_id(df)

    new_row = pd.DataFrame([{COL_ID: exp_id, COL_DATE: today, COL_AMOUNT: amount, COL_CATEGORY: category, COL_NOTE: note}])
    df = pd.concat([df, new_row], ignore_index=True)
    save_expenses(df)

    print(f"\n  ✅  Expense #{exp_id} saved!  ${amount:.2f} · {category} · {today}")
    return df

def view_all(df: pd.DataFrame) -> None:
    print("\n" + "─" * WIDTH)
    print("  📋  ALL EXPENSES")
    print("─" * WIDTH)

    if df.empty:
        print("  No expenses recorded yet.")
        return

    display = df[[COL_ID, COL_DATE, COL_AMOUNT, COL_CATEGORY, COL_NOTE]].copy()
    display[COL_DATE] = pd.to_datetime(display[COL_DATE]).dt.strftime("%Y-%m-%d")
    display[COL_AMOUNT] = display[COL_AMOUNT].apply(lambda x: f"${x:>8.2f}")
    display.columns = ["ID", "Date", "Amount", "Category", "Note"]
    display = display.fillna("")
    print(display.to_string(index=False))
    hr()
    print(f"  Grand total: ${df[COL_AMOUNT].sum():,.2f} ({len(df)} records)")
    hr()

def view_monthly(df: pd.DataFrame) -> None:
    print("\n" + "─" * WIDTH)
    print("  📅  MONTHLY TOTALS")
    print("─" * WIDTH)

    if df.empty:
        print("  No expenses recorded yet.")
        return

    month, year = prompt_month_year()
    df_month = df[(pd.to_datetime(df[COL_DATE]).dt.month == month) &
                  (pd.to_datetime(df[COL_DATE]).dt.year == year)].copy()
    month_label = datetime(year, month, 1).strftime("%B %Y")

    if df_month.empty:
        print(f"\n  No expenses for {month_label}.")
        return

    print(f"\n  Results for: {month_label}")
    hr()

    cat_totals = df_month.groupby(COL_CATEGORY)[COL_AMOUNT].sum().sort_values(ascending=False).reset_index()
    cat_totals.columns = ["Category", "Total"]

    print(f"  {'Category':<28}  {'Total':>10}")
    hr("·")
    for _, row in cat_totals.iterrows():
        print(f"  {row['Category']:<28}  ${row['Total']:>9.2f}")
    hr()

    monthly_total = df_month[COL_AMOUNT].sum()
    avg_per_day = monthly_total / df_month[COL_DATE].nunique()
    print(f"  {'Month total':<28}  ${monthly_total:>9.2f}")
    print(f"  {'Average per active day':<28}  ${avg_per_day:>9.2f}")
    print(f"  {'Number of transactions':<28}  {len(df_month):>10}")
    hr()

def view_by_category(df: pd.DataFrame) -> None:
    print("\n" + "─" * WIDTH)
    print("  🏷️   SPENDING BY CATEGORY  (all time)")
    print("─" * WIDTH)

    if df.empty:
        print("  No expenses recorded yet.")
        return

    cat_totals = df.groupby(COL_CATEGORY)[COL_AMOUNT].agg(["sum", "count"]).rename(columns={"sum": "total", "count": "txns"}).sort_values("total", ascending=False).reset_index()
    grand_total = cat_totals["total"].sum()
    max_total = cat_totals["total"].max()
    bar_width = 20

    print(f"\n  {'Category':<22} {'Total':>9}  {'%':>5}  Bar")
    hr("·")
    for _, row in cat_totals.iterrows():
        pct = (row["total"] / grand_total * 100) if grand_total else 0
        bar_len = int((row["total"] / max_total) * bar_width) if max_total else 0
        bar = "█" * bar_len
        print(f"  {row[COL_CATEGORY]:<22} ${row['total']:>8.2f}  {pct:>4.1f}%  {bar}")
    hr()
    print(f"  {'TOTAL':<22} ${grand_total:>8.2f}  100.0%")
    hr()

def delete_expense(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "─" * WIDTH)
    print("  🗑️   DELETE AN EXPENSE")
    print("─" * WIDTH)

    if df.empty:
        print("  No expenses to delete.")
        return df

    view_all(df)
    raw = input("\n  Enter the ID to delete (or press Enter to cancel): ").strip()
    if not raw:
        print("  ↩️   Cancelled.")
        return df
    if not raw.isdigit():
        print("  ⚠️  Invalid ID.")
        return df

    exp_id = int(raw)
    if exp_id not in df[COL_ID].values:
        print(f"  ⚠️  No expense found with ID {exp_id}.")
        return df

    row = df[df[COL_ID] == exp_id].iloc[0]
    print(f"\n  About to delete: ID {exp_id} · ${row[COL_AMOUNT]:.2f} · {row[COL_CATEGORY]} · {row[COL_DATE]}")
    if input("  Confirm delete? [y/N]: ").strip().lower() != "y":
        print("  ↩️   Cancelled.")
        return df

    df = df[df[COL_ID] != exp_id].reset_index(drop=True)
    save_expenses(df)
    print(f"  ✅  Expense #{exp_id} deleted.")
    return df

def run() -> None:
    banner()
    print(f"\n  Data file: {os.path.abspath(CSV_FILE)}")
    df = load_expenses()
    print(f"  {len(df)} expense(s) loaded.\n")

    while True:
        menu()
        choice = input("  Choose an option (1–6): ").strip()
        if choice == "1":
            df = add_expense(df)
        elif choice == "2":
            view_all(df)
        elif choice == "3":
            view_monthly(df)
        elif choice == "4":
            view_by_category(df)
        elif choice == "5":
            df = delete_expense(df)
        elif choice == "6":
            print("\n  Goodbye! Keep tracking those expenses. 👋\n")
            sys.exit(0)
        else:
            print("  ⚠️  Invalid choice. Enter 1–6.")

if __name__ == "__main__":
    run()