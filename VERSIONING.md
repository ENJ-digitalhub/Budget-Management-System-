## ENJ0Y Budget CLI – Version History

This document tracks the evolution of the ENJ0Y Budget CLI project using semantic versioning principles.

---

## Versioning Format

The project follows Semantic Versioning:

MAJOR.MINOR.PATCH

- MAJOR (x.0.0): Breaking changes or major architectural updates  
- MINOR (0.x.0): New features or integrations  
- PATCH (0.0.x): Bug fixes and small improvements  

---

## Release History

---

### v1.0.0 – Initial Application Release

The first working version of the ENJ0Y Budget CLI system.

**Features:**
- Core CLI application setup
- Basic budget tracking system
- Add income and expense functionality
- Initial command routing system
- Simple internal data handling

**Summary:**
Foundation build of the application. Core logic and structure established.

---

### v1.1.0 – Report Function Integration

Introduced reporting capabilities to improve financial insight.

**Features:**
- Added report generation system
- Summary of income and expenses
- Improved CLI output formatting
- Better structured financial data display

**Summary:**
This update transforms raw financial entries into readable insights through reports.

---

### v1.2.0 – Entry Point Integration

Major structural improvement introducing a defined application entry point.

**Features:**
- Added centralized entry point (`init` or main bootstrap flow)
- Improved application startup architecture
- Better separation of initialization logic and core modules
- Cleaner execution flow for CLI commands
- Improved project structure consistency

**Summary:**
This version restructures how the application starts and runs, making the system more scalable and maintainable.

---

### v1.3.0 – Delete Function & Remove Function Adjustment Integration

This version introduces data deletion capabilities and improves the logic behind the remove functionality for better accuracy and control.

**Features:**
- Added delete function for removing specific records from the system
- Improved remove function behavior for more precise data handling
- Enhanced validation to prevent accidental or invalid deletions
- Fixed inconsistencies between "remove" and "delete" command logic
- Improved internal data update flow after deletions
- Strengthened safety checks before destructive operations

**Summary:**
This update introduces controlled data removal capabilities and refines existing removal logic. It ensures that data deletion is intentional, consistent, and safer across the system while maintaining system stability.

---

## Versioning Philosophy

This project follows a structured evolution approach:

- Stability first: core system must always remain functional
- Features are added incrementally
- Architecture improves over time, not all at once
- Each version should be traceable and reversible

---

## Future Roadmap (Planned)

- Persistent storage system (file-based or database)
- Advanced analytics and reporting expansion
- Export functionality (CSV / Excel)
- Plugin or module-based architecture
- Improved error handling system

---

## Notes

- Always update version numbers before pushing changes
- Avoid skipping minor versions for feature additions
- PATCH versions should only be used for fixes or corrections