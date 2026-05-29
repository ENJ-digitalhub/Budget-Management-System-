class Help:
	def helpMessage(self):
		print("\n" + "="*50)
		print("QUICK COMMAND REFERENCE")
		print("="*50)

		print("\nFORMAT:")
		print("  [category] [action] [id?] [amount?] [label?]")

		print("\nCATEGORIES:")
		print("  allowance, expenses, income, savings")

		print("\nACTIONS:")
		print("  add, remove, delete, modify, show, total, status, search, report")

		print("\nEXAMPLES:")
		print("  allowance add 1000")
		print("  expenses add 1500 lunch")
		print("  expenses remove 1500 lunch_returned")
		print("  expenses delete 5")
		print("  expenses modify 3 200 dinner")
		print("  expenses show")
		print("  expenses total 2026-12")
		print("  expenses status 2026-12-05")
		print("  expenses search lunch")
		print("  report 2026-02")

		print("\nIMPORTANT:")
		print("  • Labels must be alphanumeric (a-z, 0-9) only")
		print("  • Labels with space must be put in quotes")
		print("  • Amount must be numeric")

		print("\nType 'help detailed' for full documentation")
		print("="*50 + "\n")


	def detailedHelp(self):
		print("\n" + "="*60)
		print("BUDGET CLI - DETAILED COMMAND REFERENCE")
		print("="*60)

		print("\nCOMMAND FORMAT:")
		print("  [category] [action] [parameters...]")

		print("\nACTION STRUCTURES:")
		print("  add      -> [category] add [amount] [label?]")
		print("  remove   -> [category] remove [amount] [label]")
		print("  delete   -> [category] delete [id]")
		print("  modify   -> [category] modify [id] [amount] [label?]")
		print("  show     -> [category] show")
		print("  total    -> [category] total [YYYY-MM | YYYY-MM-DD]")
		print("  search   -> [category] search [label]")
		print("  status   -> status [YYYY-MM-DD]")
		print("  report   -> report [YYYY-MM | YYYY]")

		print("\nCATEGORIES:")
		print("  • allowance  - Base budget allocation")
		print("  • expenses   - Spending records")
		print("  • income     - Income entries")
		print("  • savings    - Savings tracking")

		print("\nCORE BEHAVIOR:")
		print("  • add     = create new record")
		print("  • remove  = soft adjustment (creates negative transaction)")
		print("  • delete  = permanent removal (by ID)")
		print("  • modify  = update existing record")

		print("\nEXAMPLES:")

		print("\n  Add:")
		print("    allowance add 1000")
		print("    expenses add 1500 lunch")

		print("\n  Remove (adjustment):")
		print("    expenses remove 1500 lunch_returned")

		print("\n  Delete (hard remove):")
		print("    expenses delete 5")

		print("\n  Modify:")
		print("    expenses modify 3 200 dinner")

		print("\n  Totals:")
		print("    expenses total")
		print("    expenses total 2026-12")

		print("\n  Search:")
		print("    expenses search snacks")

		print("\n  Status:")
		print("    status 2026-02-05")
		print("    status 2026")

		print("\n  Reports:")
		print("    report 2026-02")
		print("    report 2026")

		print("\nVALIDATION RULES:")
		print("  • Amount must be numeric (e.g., 100, 2500)")
		print("  • ID must be numeric (for delete/modify)")
		print("  • Labels must match: [a-zA-Z0-9]+")
		print("  • Labels must be contained quotes")
		print("  • Commands are case-insensitive")

		print("\nNOTES:")
		print("  • 'remove' does NOT delete data (audit-safe)")
		print("  • 'delete' permanently removes a record")
		print("  • Allowance should be set before other categories")

		print("\nGENERAL COMMANDS:")
		print("  • help           - Quick help")
		print("  • help detailed  - Full documentation")
		print("  • quit           - Exit app")
		print("  • logout         - Exit session")

		print("\n" + "="*60)
		print("TIP: This system uses a transaction-based ledger model")
		print("="*60 + "\n")