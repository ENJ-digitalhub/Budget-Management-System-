package BMS;

import java.io.*;
import java.util.*;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDateTime;

public class SystemUtils {
	private static boolean isConfirm = false;
	static Scanner read = new Scanner(System.in);
	static LocalDateTime time = LocalDateTime.now();
	static Map<Character, int[]> letterIndexes = new HashMap<>();

	public static String center(String s, double width) {
		double padding = (width - s.length()) / 2;
		return " ".repeat((int) padding) + s + " ".repeat((int) padding);
	}
	public static void clearScreen() {
		try {
			if (System.getProperty("os.name").contains("Windows")) {
				new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
			} else {
				System.out.print("\033[H\033[2J");
				System.out.flush();
			}
		} catch (Exception e) {
			for (int i = 0; i < 50; i++) System.out.println();
		}
	}
	public static void exit() {
		clearScreen();
		System.out.println("Closing program . . .");
	}
	public static boolean confirm(Object x) {
		clearScreen();
		System.out.print("Confirm \"" + x + "\" (Y/N)? ");
		char confirm = read.next().charAt(0);
		confirm = Character.toLowerCase(confirm);
		if (confirm == 'y') {
			clearScreen();
			System.out.println("Confirmed . . .");
			isConfirm = true;
		} else if (confirm == 'n') {
			clearScreen();
			System.out.println(". . .");
			isConfirm = false;
		} else {
			clearScreen();
			System.out.println("Invalid Input");
			confirm(x);
		}
		return isConfirm;
	}
	public static String encrypt(String pin) {
		if (pin.length() != 4) throw new IllegalArgumentException("PIN must be 4 digits");
		int d1 = Integer.parseInt("" + pin.charAt(0));
		int d2 = Integer.parseInt("" + pin.charAt(1));
		int d3 = Integer.parseInt("" + pin.charAt(2));
		int d4 = Integer.parseInt("" + pin.charAt(3));

		int temp = d1; d1 = d3; d3 = temp;
		temp = d2; d2 = d4; d4 = temp;

		d1 = (d1 + 7) % 10;
		d2 = (d2 + 7) % 10;
		d3 = (d3 + 7) % 10;
		d4 = (d4 + 7) % 10;

		int encryptedPin = (d1 * 1000) + (d2 * 100) + (d3 * 10) + d4;
		return String.format("%04d", encryptedPin);
	}
	public static String decrypt(String ePin) {
		if (ePin.length() != 4) throw new IllegalArgumentException("Encrypted PIN must be 4 digits");
		int d1 = Integer.parseInt("" + ePin.charAt(0));
		int d2 = Integer.parseInt("" + ePin.charAt(1));
		int d3 = Integer.parseInt("" + ePin.charAt(2));
		int d4 = Integer.parseInt("" + ePin.charAt(3));

		int temp = d1; d1 = d3; d3 = temp;
		temp = d2; d2 = d4; d4 = temp;

		d1 = (d1 + 3) % 10;
		d2 = (d2 + 3) % 10;
		d3 = (d3 + 3) % 10;
		d4 = (d4 + 3) % 10;

		int decryptedPin = (d1 * 1000) + (d2 * 100) + (d3 * 10) + d4;
		return String.format("%04d", decryptedPin);
	}
	public static String monthsOfTheYear(String date) {
		String[] parts = date.split("-");
		int month = Integer.parseInt(parts[1]);
		LocalDateTime monthObj = time.withMonth(month);
		return monthObj.getMonth().toString();
	}
	public static double getPositiveDoubleInput(String prompt) {
		double value = -1;
		do {
			System.out.print(prompt);
			try { value = read.nextDouble(); read.nextLine().trim(); } 
			catch (Exception e) { System.out.println("Invalid input."); read.nextLine().trim(); value = -1; }
		} while (value < 0);
		return value;
	}
	public static int getPositiveIntInput(String prompt) {
		int value = -1;
		do {
			System.out.print(prompt);
			try { value = read.nextInt(); read.nextLine().trim(); } 
			catch (Exception e) { System.out.println("Invalid input."); read.nextLine().trim(); value = -1; }
		} while (value < 0);
		return value;
	}
	/** Reads all rows from a table */
	public static ArrayList<ArrayList<Object>> readTable(String tableName) {
		ArrayList<ArrayList<Object>> records = new ArrayList<>();
		try (Connection conn = Database.connect();
			 Statement stmt = conn.createStatement();
			 ResultSet rs = stmt.executeQuery("SELECT * FROM " + tableName)) {

			int columnCount = rs.getMetaData().getColumnCount();
			while (rs.next()) {
				ArrayList<Object> row = new ArrayList<>();
				for (int i = 1; i <= columnCount; i++) row.add(rs.getObject(i));
				records.add(row);
			}
		} catch (SQLException e) { e.printStackTrace(); }
		return records;
	}
	/** Adds a record to a table
	Adds a record to a table - automatically adds created_by with current username */
	public static void addRecord(String tableName, Object[] values) {
		Connection conn = null;
		PreparedStatement pstmt = null;
		
		try {
			conn = Database.connect();
			if (conn == null) {
				System.err.println("Cannot connect to database to add record");
				return;
			}
			
			// Get current username (you need to implement this in User class)
			String currentUsername = User.userUserName;
			
			// Handle different table schemas
			if (tableName.equalsIgnoreCase("inventory")) {
				// Inventory table has: inventory_id, bird_no, eggs_no, feeds_no, created_by, created_at
				// We need to provide: bird_no, eggs_no, broken_eggs, feeds_no, created_by
				String sql = "INSERT INTO inventory (bird_no, eggs_no, broken_eggs, feeds_no, created_by) VALUES (?, ?, ?, ?, ?)";
				pstmt = conn.prepareStatement(sql);
				
				// Check how many values were provided
				if (values.length == 4) {
					// User provided: bird_no, eggs_no, broken_eggs,feeds_no
					pstmt.setObject(1, values[0]);
					pstmt.setObject(2, values[1]);
					pstmt.setObject(3, values[2]);
					pstmt.setObject(4, values[3]);
					pstmt.setString(5, currentUsername);
				} else if (values.length == 5) {
					// User already included created_by
					for (int i = 0; i < 5; i++) pstmt.setObject(i + 1, values[i]);
				} else {
					System.err.println("Wrong number of values for inventory table. Expected 4 or 5, got " + values.length);
					return;
				}
				
				pstmt.executeUpdate();
				
			} else if (tableName.equalsIgnoreCase("farm_records")) {
				// Farm_records has: record_id, record_date, eggs_collected, feeds_used, death, comment, created_by, created_at
				// We need to provide: record_date, eggs_collected, feeds_used, death, comment, created_by
				String sql = "INSERT INTO farm_records (eggs_collected, broken_eggs, feeds_used, death, comment, created_by) VALUES (?, ?, ?, ?, ?, ?)";
				pstmt = conn.prepareStatement(sql);
				
				if (values.length == 5) {
					// User provided:eggs_collected, broken_eggs, feeds_used, death, comment
					pstmt.setObject(1, values[0]);
					pstmt.setObject(2, values[1]);
					pstmt.setObject(3, values[2]);
					pstmt.setObject(4, values[3]);
					pstmt.setObject(5, values[4]);
					pstmt.setString(6, currentUsername);
				} else if (values.length == 6) {
					// User already included created_by
					for (int i = 0; i < 6; i++) pstmt.setObject(i + 1, values[i]);
				} else {
					System.err.println("Wrong number of values for farm_records table. Expected 5 or 6, got " + values.length);
					return;
				}
				
				pstmt.executeUpdate();
				System.out.println("Farm record added Succesfully. " );
				
			} else {
				// For other tables: use original logic
				String placeholders = String.join(",", Collections.nCopies(values.length, "?"));
				String sql = "INSERT INTO " + tableName + " VALUES (NULL," + placeholders + ")";
				pstmt = conn.prepareStatement(sql);
				for (int i = 0; i < values.length; i++) pstmt.setObject(i + 1, values[i]);
				pstmt.executeUpdate();
				System.out.println("Record added to " + tableName);
			}
			
		} catch (SQLException e) { 
			System.err.println("Error adding record to " + tableName + ": " + e.getMessage());
			e.printStackTrace(); 
		} finally {
			try {
				if (pstmt != null) pstmt.close();
			} catch (SQLException e) {
				System.err.println("Error closing statement: " + e.getMessage());
			}
			try {
				if (conn != null) conn.close();
			} catch (SQLException e) {
				System.err.println("Error closing connection: " + e.getMessage());
			}
		}
	}
	/** Updates record(s) in table - automatically updates created_by with current username */
	public static void updateRecord(String tableName, String[] columnNames, Object[] values, String condition) {
		if (columnNames.length != values.length) { 
			System.out.println("Column names and values mismatch!"); 
			return; 
		}
		
		Connection conn = null;
		PreparedStatement pstmt = null;
		
		try {
			conn = Database.connect();
			if (conn == null) {
				System.err.println("Cannot connect to database to update record");
				return;
			}
			
			// Get current username
			String currentUsername = User.userUserName;
			
			// Check if this table has created_by column and if we need to update it
			boolean hasCreatedBy = tableName.equalsIgnoreCase("inventory") || 
								  tableName.equalsIgnoreCase("farm_records");
			boolean userProvidedCreatedBy = false;
			
			// Check if user already provided created_by in columnNames
			for (String col : columnNames) {
				if (col.equalsIgnoreCase("created_by")) {
					userProvidedCreatedBy = true;
					break;
				}
			}
			
			StringBuilder sql = new StringBuilder("UPDATE " + tableName + " SET ");
			
			// Add user-specified columns
			for (int i = 0; i < columnNames.length; i++) { 
				sql.append(columnNames[i]).append("=?"); 
				if (i < columnNames.length - 1) sql.append(", "); 
			}
			
			// Add created_by if needed (for inventory and farm_records tables)
			if (hasCreatedBy && !userProvidedCreatedBy) {
				if (columnNames.length > 0) sql.append(", ");
				sql.append("created_by=?");
			}
			
			sql.append(" WHERE ").append(condition);
			
			System.out.println("Executing: " + sql.toString());
			
			pstmt = conn.prepareStatement(sql.toString());
			
			// Set user-specified values
			for (int i = 0; i < values.length; i++) {
				pstmt.setObject(i + 1, values[i]);
			}
			
			// Add created_by value if needed
			if (hasCreatedBy && !userProvidedCreatedBy) {
				pstmt.setString(values.length + 1, currentUsername);
			}
			
			int rowsUpdated = pstmt.executeUpdate();
			System.out.println("✓ " + rowsUpdated + " record(s) updated in " + tableName);
			if (hasCreatedBy && !userProvidedCreatedBy) {
				System.out.println("✓ Updated Succesfully");
			}
			
		} catch (SQLException e) { 
			System.err.println("Error updating record in " + tableName + ": " + e.getMessage());
			e.printStackTrace(); 
		} finally {
			try {
				if (pstmt != null) pstmt.close();
			} catch (SQLException e) {
				System.err.println("Error closing statement: " + e.getMessage());
			}
			try {
				if (conn != null) conn.close();
			} catch (SQLException e) {
				System.err.println("Error closing connection: " + e.getMessage());
			}
		}
	}
	/** Checks if a record exists in a table */
	public static boolean recordExists(String tableName, String columnName, Object value) {
		String sql = "SELECT 1 FROM " + tableName + " WHERE " + columnName + " = ? LIMIT 1";
		try (Connection conn = Database.connect();
			 PreparedStatement pstmt = conn.prepareStatement(sql)) {
			pstmt.setObject(1, value);
			try (ResultSet rs = pstmt.executeQuery()) { return rs.next(); }
		} catch (SQLException e) { e.printStackTrace(); }
		return false;
	}
	/** Gets all records as Object[][] (for FarmRecord view) */
	public static Object[][] getAllRecords(String tableName) {
		ArrayList<Object[]> list = new ArrayList<>();
		try (Connection conn = Database.connect();
			 Statement stmt = conn.createStatement();
			 ResultSet rs = stmt.executeQuery("SELECT * FROM " + tableName)) {
			int cols = rs.getMetaData().getColumnCount();
			while (rs.next()) {
				Object[] row = new Object[cols];
				for (int i = 1; i <= cols; i++) row[i-1] = rs.getObject(i);
				list.add(row);
			}
		} catch (SQLException e) { e.printStackTrace(); }
		return list.toArray(new Object[0][]);
	}
	/** Gets single record by date */
	public static Object[] getRecordByDate(String tableName, String dateColumn, String date) {
		try (Connection conn = Database.connect()) {
			String sql = "SELECT * FROM " + tableName + " WHERE " + dateColumn + " = ?";
			PreparedStatement pstmt = conn.prepareStatement(sql);
			pstmt.setString(1, date);
			ResultSet rs = pstmt.executeQuery();
			int cols = rs.getMetaData().getColumnCount();
			if (rs.next()) {
				Object[] row = new Object[cols];
				for (int i = 1; i <= cols; i++) row[i-1] = rs.getObject(i);
				return row;
			}
		} catch (SQLException e) { e.printStackTrace(); }
		return null;
	}
	/** Returns a paginated sublist from an ArrayList */
	public static <T> ArrayList<T> getPage(ArrayList<T> records, int page, int pageSize) {
		int fromIndex = (page - 1) * pageSize;
		int toIndex = Math.min(fromIndex + pageSize, records.size());
		if (fromIndex >= records.size()) return new ArrayList<>();
		return new ArrayList<>(records.subList(fromIndex, toIndex));
	}
	public static void printLetterFromIndexes(int[] filledIndexes) {
		int rows = 6;
		int cols = 5;
		char[][] board = new char[rows][cols];

		// Initialize all holes to empty
		for (int r = 0; r < rows; r++) {
			for (int c = 0; c < cols; c++) {
				board[r][c] = ' ';
			}
		}

		// Fill the specified holes
		for (int index : filledIndexes) {
			if (index < 1 || index > rows * cols) continue; // ignore invalid indexes
			int r = (index - 1) / cols;
			int c = (index - 1) % cols;
			board[r][c] = 'X';
		}

		// Print the board
		for (int r = 0; r < rows; r++) {
			for (int c = 0; c < cols; c++) {
				System.out.print(board[r][c] + " ");
			}
			System.out.println();
		}
	}
		// Load letters from file
	public static void loadLetters(String filename) {
		try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
			String line;
			while((line = br.readLine()) != null) {
				line = line.trim();
				if(line.isEmpty()) continue;
				String[] parts = line.split(":");
				if(parts.length != 2) continue;
				char letter = parts[0].charAt(0);
				String[] nums = parts[1].split(",");
				int[] indexes = new int[nums.length];
				for(int i=0;i<nums.length;i++){
					indexes[i] = Integer.parseInt(nums[i].trim());
				}
				letterIndexes.put(letter, indexes);
			}
		} catch(IOException e){
			System.out.println("Error reading letters file: " + e.getMessage());
		}
	}
	public static char[][] buildLetterGrid(char letter) {
		int rows = 6;
		int cols = 5;
		char[][] grid = new char[rows][cols];
		for(int r=0;r<rows;r++){
			Arrays.fill(grid[r],' ');
		}
		int[] indexes = letterIndexes.get(letter);
		if(indexes != null){
			for(int idx : indexes){
				int r = (idx-1)/cols;
				int c = (idx-1)%cols;
				grid[r][c] = 'X';
			}
		}
		return grid;
	}
	public static void printWordHorizontal(String word) {
		int rows = 6;
		int cols = 5;
		char[][][] grids = new char[word.length()][][];
		for(int i=0;i<word.length();i++){
			grids[i] = buildLetterGrid(word.charAt(i));
		}
		for(int r=0;r<rows;r++){
			for(int l=0;l<word.length();l++){
				for(int c=0;c<cols;c++){
					System.out.print(grids[l][r][c]);
				}
				System.out.print("  "); // space between letters
			}
			System.out.println();
		}
	}
}
