class Help:
	def helpMessage(self):
		print("\n" + "="*50)
		print("QUICK COMMAND REFERENCE")
		print("="*50)

		print("\nFORMAT: [category] [action] [id] [amount] [label]")

		print("\nCATEGORIES: allowance, expenses, income, savings")
		print("ACTIONS: add, remove, modify, delete, show, total, status, search")

		print("\nEXAMPLES:")
		print("  allowance add 1000")
		print("  expenses add 1500 lunch")
		print("  expenses remove 1500 lunch_returned")
		print("  expenses delete 5")
		print("  expenses modify 3 20 dinner")
		print("  expenses show")
		print("  expenses total 2026-12")
		print("  expenses total 2026-12-05")
		print("  expenses status 2026-12-05")
		print("  allowance search transport")
		print("  report 2026-02 (February 2026)")

		print("\nType 'help detailed' for full documentation")
		print("="*50 + "\n")

	def detailedHelp(self):
		print("\n" + "="*60)
		print("BUDGET CLI - DETAILED COMMAND REFERENCE")
		print("="*60)

		print("\nCOMMAND FORMAT:")
		print("  [category] [action] [id] [amount] [label]")
		print("  • total   -> [category] total [YYYY-MM]")
		print("  • status  -> [category] status [YYYY-MM-DD]")
		print("  • search  -> [category] search [label]")
		print("  • report  -> report [YYYY-MM] or report [YYYY]")

		print("\nCATEGORIES:")
		print("  • allowance  - Base budget allocation")
		print("  • expenses   - Spending records")
		print("  • income     - Income entries")
		print("  • savings    - Savings deposits/withdrawals")

		print("\nACTIONS:")
		print("  • add     - Create new record")
		print("  • remove  - Remove record (adjustment with negative amount)")
		print("  • delete  - Permanently delete record (new integration)")
		print("  • modify  - Update record by ID")
		print("  • show    - List all records")
		print("  • total   - Compute totals by category/time")
		print("  • status  - Show financial balance snapshot")
		print("  • search  - Query by label text")
		print("  • report  - Generate summary report")

		print("\nEXAMPLES:")
		print("  Add records:")
		print("    allowance add 1000")
		print("    expenses add 1500 lunch")
		print("    income add 200 freelance")

		print("\n  Remove/Delete:")
		print("    expenses remove 1500 lunch_returned")
		print("    expenses delete 5")

		print("\n  Modify:")
		print("    expenses modify 3 20 dinner")

		print("\n  Totals:")
		print("    expenses total")
		print("    income total 2026-12")

		print("\n  Status:")
		print("    expenses status 2026-02-05")
		print("    status 2026-02")

		print("\n  Search:")
		print("    expenses search snacks")
		print("    allowance search transport")

		print("\n  Reports:")
		print("    report 2026-02")
		print("    report 2026")

		print("\nDATABASE RELATIONSHIPS:")
		print("  • Records are linked via timestamps (created_at = record_date)")
		print("  • Expenses, income, and savings depend on allowance baseline")
		print("  • Allowance should be initialized first for consistency")

		print("\nIMPORTANT NOTES:")
		print("  • ID is required for modify/delete actions")
		print("  • Amount must be numeric")
		print("  • Label is optional except where required by category rules")
		print("  • Date formats: YYYY-MM or YYYY-MM-DD")
		print("  • Commands are case-insensitive")
		print("  • delete = hard removal, remove = soft/legacy behavior")

		print("\nGENERAL COMMANDS:")
		print("  • help           - Quick help")
		print("  • help detailed  - Full documentation")
		print("  • quit           - Exit app")
		print("  • logout         - Exit account session")

		print("\n" + "="*60)
		print("TIP: Keep command schema aligned with database.py to avoid drift")
		print("="*60 + "\n")