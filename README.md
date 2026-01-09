# 💰 BudgetCLI – Budget Management System

![Status](https://img.shields.io/badge/Status-v1.5_Active-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/Database-SQLite-orange)
![Interface](https://img.shields.io/badge/Interface-CLI-lightgrey)

**BudgetCLI** is a **Python command-line application** built to help users track **daily allowances, budgets, expenses, income, and savings** in a structured, reliable, and efficient way.

Inspired by real-life daily budgeting records, BudgetCLI replaces complex spreadsheets with a **fast, offline, and persistent CLI tool** powered by **SQLite**.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Example Commands](#-example-commands)
- [Sample Daily Summary Output](#-sample-daily-summary-output)
- [Configuration](#-configuration-settingsjson)
- [Version Roadmap](#-version-roadmap)
- [Project Goals](#-project-goals)
- [License](#-license)
- [Author](#-author)

---

## 📌 Features

### 🔹 Daily Budget Management
- Set daily allowance
- Define transport and diet budgets
- Record actual transport and diet spending
- Automatic balance calculation
- Daily contribution tracking

### 🔹 Income & Expense Tracking
- Record extra income (e.g., gifts, payments, change)
- Record extra expenses (e.g., airtime, USSD charges, levies)
- Multiple income and expense entries per day
- Clearly labeled transactions for easy review

### 🔹 Reporting
- Full daily summary (spreadsheet-style output)
- Monthly summaries with subtotals
- Net daily and monthly balance calculation
- Overspending alerts and negative balance indicators

### 🔹 Configuration
- JSON-based settings file
- Default budgets and contribution values
- Configurable currency symbol

### 🔹 Data Persistence
- SQLite database for all financial records
- Automatic table creation on first run
- Safe, offline-first storage

---

## 🛠 Tech Stack

| Component | Technology |
|---------|-----------|
| Language | Python |
| Database | SQLite |
| Configuration | JSON |
| Interface | Command Line (CMD / Terminal) |

---

## 📂 Project Structure

```text
BudgetCLI/
├── data/
│   └── budget.db            # SQLite database
├── config/
│   └── settings.json        # Application configuration
├── src/
│   ├── app/                 # Application entry point
│   ├── commands/            # CLI command handlers
│   ├── db/                  # Database connection & queries
│   ├── models/              # Data models
│   └── utils/               # Helper utilities
└── README.md
```

---

## 🚀 Example Commands

day start 2025-08-04
allowance set 2500
budget transport 1500
budget diet 200
spend transport 1000
spend diet 300
income add "SIR HUMBLE" 1300
expense add "Airtime" 300
contribution set 500
day summary


---

## 📊 Sample Daily Summary Output

**DATE:** Monday, August 4, 2025

**Allowance:** ₦2,500

**Transport:**
  **Budget:** ₦1,500
  **Paid:** ₦1,000
  **Balance:** ₦500

**Diet:**
  **Budget:** ₦200
  **Spent:** ₦300
  **Balance:** -₦100

**Extra Income:**
  **SIR HUMBLE:** ₦1,300

**Extra Expenses:**
  **Airtime:** ₦300

**Contribution:** ₦500

**NET TOTAL:** ₦2,000


---

## ⚙ Configuration (settings.json)

{
  "currency": "₦",
  "dailyContribution": 500,
  "defaultBudgets": {
    "transport": 1500,
    "diet": 200
  },
  "database": {
    "path": "data/budget.db"
  }
}


---

## 🧩 Version Roadmap

### v1.0

Daily budgeting

Income and expense tracking

SQLite persistence

Daily summary reports


### v1.5

Monthly summaries

CSV export

Backup and restore support


### v2.0

Advanced analytics

PIN-based protection

Optional multi-user support



---

## 🎯 Project Goals

Replace manual spreadsheet budgeting

Encourage daily financial discipline

Provide clear visibility into spending habits

Serve as a portfolio-grade Python CLI project



---

## 📄 License

This project is licensed under the MIT License — free to use, modify, and distribute with proper attribution.


---

## 👤 Author

ENJ-digitalhub
Python Developer | CLI & Systems Projects
