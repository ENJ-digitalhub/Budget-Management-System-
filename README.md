# 💰 ENJ0Y Budget CLI – Budget Management System

![Status](https://img.shields.io/badge/Status-v1.4.0_Active-green)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Database](https://img.shields.io/badge/Storage-File%20%7C%20SQLite_(Planned)-orange)
![Interface](https://img.shields.io/badge/Interface-CLI-lightgrey)

**ENJ0Y Budget CLI** is a transaction-based command-line financial tracking system designed to help users manage allowances, expenses, income, and savings with precision, safety, and structured data flow.

Built with a strong focus on data integrity, validation, and modular architecture, the system evolves incrementally using semantic versioning principles.

---

## 📑 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Command System](#️-command-system)
- [Example Commands](#-example-commands)
- [Core Design Philosophy](#-design-philosophy)
- [Version History](#-version-history)
- [Roadmap](#-roadmap)
- [Author](#-author)

---

## 📌 Features

### Transaction-Based Ledger System

- Every operation is recorded as a transaction
- “Remove” creates adjustment entries (audit-safe)
- “Delete” performs permanent removal (controlled)

### Budget & Financial Tracking

- Allowance management (base budget)
- Expense tracking with labels
- Income tracking
- Savings tracking
- Multiple entries per category

### Data Integrity (v1.4.0)

- Strict validation layer for all inputs
- Integrity checks on create, update, delete
- Protection against inconsistent data states
- Improved error handling and system reliability

### Reporting & Insights

- Category-based summaries
- Monthly and daily totals
- Search and filtering capabilities
- Report generation by date

### CLI Command Engine

- Structured command parsing
- Category + action-based execution
- Modular command routing system

---

## 🛠 Tech Stack

Component| Technology
Language| Python
Interface| Command Line (CLI)
Storage| In-memory → File/DB (Planned)
Validation| Custom validation module
Architecture| Modular (Command-driven)

---

## 📂 Project Structure

```
ENJOY_BudgetCLI/
├── src/
│   └── budgetcli/
│       ├── app.py              # Entry point (bootstrap system)
│       ├── commands.py         # Command parsing & execution
│       ├── database.py         # Data access layer (SQL/file abstraction)
│       ├── config.py           # Config loader interface
│       ├── validator.py        # Input validation layer
│       ├── user.py             # Auth/session handling
│       ├── help.py             # CLI help system
│       └── utils/              # shared helpers (optional growth folder)

├── data/
│   ├── budget.db               # main database file (or user.db consolidated)
│   ├── users/                 # user-specific files if needed
│   │   ├── userA/
│   │   ├── userB/
│   │   └── ...

├── config/
│   └── settings.json          # application configuration

├── tests/                      # (future: unit tests)
├── pyproject.toml
└── README.md
```

---

## ⚙️ Command System

### Format

[category] [action] [parameters...]

#### Categories

- allowance
- expenses
- income
- savings

#### Actions

- add
- remove
- delete
- modify
- show
- total
- status
- search
- report

---

### 🧪 Example Commands

allowance add 1000
expenses add 1500 lunch
expenses remove 1500 lunch_returned
expenses delete 5
expenses modify 3 200 dinner
expenses show
expenses total 2026-12
expenses status 2026-12-05
expenses search lunch
report 2026-02

---

### ⚠️ Validation Rules

- Amount must be numeric
- ID must be numeric
- Labels must match: "[a-zA-Z0-9]+"
- Labels with spaces must be quoted
- Commands are case-insensitive

---

### 🧠 Core Behavior

Action| Behavior
add| Creates a new record
remove| Creates adjustment (non-destructive)
delete| Permanently removes record
modify| Updates existing record

---

### 🧩 Design Philosophy

- Stability first — system must always run
- Incremental feature growth
- Strong validation before execution
- Clear separation of concerns
- Audit-safe financial tracking
- Predictable and reversible changes

---

## 📦 Version History

### v1.0.0 – Initial Application Release

- Core CLI system
- Basic budget tracking
- Command routing
- Foundational architecture

---

### v1.1.0 – Report Function Integration

- Reporting system added
- Financial summaries
- Improved CLI output formatting

---

### v1.2.0 – Entry Point Integration

- Centralized application entry point
- Improved startup flow
- Better architecture separation

---

### v1.3.0 – Delete & Remove Logic Upgrade

- Introduced delete functionality
- Improved remove logic (adjustments)
- Added validation for destructive operations
- Strengthened data safety

---

### v1.4.0 – Data Integrity Integration

- Full validation layer introduced
- Integrity checks across operations
- Data consistency enforcement
- Improved error handling
- Logging for inconsistencies

---

## 🚀 Roadmap

- Persistent storage (SQLite / file-based)
- Advanced analytics dashboard
- Export system (CSV / Excel)
- Authentication system expansion
- Modular plugin architecture
- API layer (future transition to web)

---

## 👤 Author

**Ekwere Noble**

---

## 📌 Notes

- Always update version before pushing changes
- Do not skip versions for feature releases
- PATCH versions = fixes only
- This system follows semantic versioning strictly