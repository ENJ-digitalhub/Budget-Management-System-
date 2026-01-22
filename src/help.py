class Help:
	def helpMessage(self):
		print("\n" + "="*50)
		print("QUICK COMMAND REFERENCE")
		print("="*50)
		
		print("\nFORMAT: [category] [action] [id] [amount] [label]")
		
		print("\nCATEGORIES: allowance, expenses, income, savings")
		print("ACTIONS: add, remove, modify, show, total")
		
		print("\nEXAMPLES:")
		print("  allowance add 1000")
		print("  expenses add 1500 'Lunch'")
		print("  expenses remove 5")
		print("  expenses modify 3 20 'Dinner'")
		print("  expenses show")
		print("  expenses total 2024-12")
		
		print("\nType 'help detailed' for full documentation")
		print("="*50 + "\n")
	def detailedHelp(self):
		print("\n" + "="*60)
		print("BUDGET CLI - DETAILED COMMAND REFERENCE")
		print("="*60)
		
		print("\nCOMMAND FORMAT:")
		print("  [category] [action] [id] [amount] [label]")
		print("  • For total: [category] total [YYYY-MM]")
		
		print("\nCATEGORIES:")
		print("  • allowance   - Daily/weekly/monthly allowance")
		print("  • expenses	- Your spending/expenses")
		print("  • income	  - Additional income sources")
		print("  • savings	 - Savings transactions")
		
		print("\nACTIONS:")
		print("  • add	 - Add a new record")
		print("  • remove  - Remove a record by ID")
		print("  • modify  - Modify a record by ID")
		print("  • show	- Show all records")
		print("  • total   - Calculate totals (optionally by month)")
		
		print("\nEXAMPLES:")
		print("  1. Add a new allowance:")
		print("	 allowance add 1000")
		
		print("\n  2. Add an expense:")
		print("	 expenses add 15 'Lunch'")
		print("	 expenses add 50 'Movie tickets'")
		
		print("\n  3. Add income:")
		print("	 income add 200 'Freelance'")
		print("	 income add 50 'Gift'")
		
		print("\n  4. Add to savings:")
		print("	 savings add 100")
		
		print("\n  5. Remove a record:")
		print("	 expenses remove 5")
		print("	 income remove 2")
		
		print("\n  6. Modify a record:")
		print("	 expenses modify 3 20 'Dinner'")
		print("	 allowance modify 1 800 ''")
		
		print("\n  7. Show all records:")
		print("	 expenses show")
		print("	 allowance show")
		print("	 income show")
		print("	 savings show")
		
		print("\n  8. Calculate totals:")
		print("	 expenses total")
		print("	 allowance total")
		print("	 income total 2024-12	(for December 2024)")
		print("	 savings total 2024-11   (for November 2024)")
		
		print("\nDATABASE RELATIONSHIPS:")
		print("  • Expenses, Income, and Savings are linked to Allowance")
		print("  • Linked by matching dates (created_at = record_date)")
		print("  • Allowance should be added first for proper linking")
		
		print("\nIMPORTANT NOTES:")
		print("  • ID parameter is required for remove/modify actions")
		print("  • Amount must be a number")
		print("  • Label is optional for most operations(except allowance and savings)")
		print("  • Month format for totals: YYYY-MM (e.g., 2024-12)")
		print("  • Dates are automatically recorded")
		print("  • Commands are case-insensitive")
		
		print("\nGENERAL COMMANDS:")
		print("  • help		   - Show quick help")
		print("  • help detailed  - Show detailed documentation")
		print("  • quit		   - Exit the application")
		
		print("\n" + "="*60)
		print("TIP: Check database structure in database.py for details")
		print("="*60 + "\n")