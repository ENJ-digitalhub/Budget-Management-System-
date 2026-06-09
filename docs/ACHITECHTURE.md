# 🧠 ENJ0Y Budget CLI – System Architecture

## Overview

The ENJ0Y Budget CLI follows a modular, command-driven architecture designed for scalability, maintainability, and data integrity.

The system processes user input through a structured pipeline:

User Input → Command Parser → Validation Layer → Command Executor → Database → Response Output

---

## 🔁 System Flow

1. User enters a CLI command
2. `app.py` receives input
3. Command is parsed using `shlex.split()`
4. `validator.py` validates structure and values
5. `commands.py` routes to appropriate executor
6. Executor performs database operation
7. Result is returned and displayed

---

## 🧩 Core Components

### app.py (Application Controller)

* Entry point of the application
* Handles:

  * Startup page
  * Login / Register flow
  * CLI loop execution
* Delegates command execution to `commands.py`

---

### commands.py (Command Engine)

* Responsible for:

  * Parsing commands
  * Mapping actions to executors
  * Executing business logic

Implements a dispatcher pattern:

```
action → method
```

Example:

```
add → addExecutor
delete → deleteExecutor
```

---

### validator.py (Validation Layer)

* Ensures all inputs meet system rules before execution
* Prevents:

  * Invalid data types
  * Malformed commands
  * Unsafe operations

Acts as a gatekeeper before database interaction

---

### database.py (Data Access Layer)

* Abstracts database operations
* Provides:

  * `run()` for execution
  * `query()` for retrieval

Ensures separation between logic and storage

---

### config.py (Configuration Manager)

* Loads and provides access to settings from `settings.json`
* Controls:

  * App metadata
  * Database settings
  * Security rules
  * Feature toggles

---

### user.py (Authentication System)

* Handles:

  * User registration
  * Login validation
  * Session management

---

### utils/ (Utility Layer)

* Provides shared helper functions such as:

  * Terminal formatting
  * Screen clearing
  * Text alignment

---

## 💾 Data Model Design

The system follows a **transaction-based ledger model**.

### Principles:

* Every action is recorded as a transaction
* No silent overwrites
* History is preserved unless explicitly deleted

### Operation Behavior:

| Action | Behavior                     |
| ------ | ---------------------------- |
| add    | Inserts positive transaction |
| remove | Inserts negative transaction |
| delete | Permanently removes record   |
| modify | Updates existing record      |

This ensures auditability and traceability.

---

## 🧠 Design Decisions

### 1. Modular Architecture

Each component has a single responsibility, improving maintainability.

---

### 2. Command Pattern

Commands are mapped dynamically to execution methods, enabling scalability.

---

### 3. Validation First Approach

No database operation occurs without validation.

---

### 4. Config-Driven System

Behavior can be adjusted without modifying code.

---

### 5. Incremental Evolution

System is designed to grow gradually using semantic versioning.

---

## 🚀 Future Improvements

* ORM integration (SQLAlchemy)
* API layer (FastAPI)
* Frontend integration (React)
* Plugin system for extensibility

---

## Conclusion

The ENJ0Y Budget CLI is structured as a scalable, secure, and extensible CLI-based financial system, with strong emphasis on data integrity, modularity, and predictable behavior.
