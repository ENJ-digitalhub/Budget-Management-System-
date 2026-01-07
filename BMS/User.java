package BMS;
import BMS.*;
import java.util.Scanner;
import java.util.Arrays;
import java.util.ArrayList;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class User{
	static Scanner read = new Scanner(System.in);
	static SystemUtils tools = new SystemUtils();
	
	static boolean isConfirm=false;
	static String firstName;
	static String lastName;
	static String userName;
	static String pin;
	public static String userFirstName;
	public static String userLastName;
	public static String userUserName;
	static String [] info = new String [4];
	static ArrayList <String> usersRecords = new ArrayList<String>();
	
	public static void register(Runnable startupPageCallBack,Runnable homecallback){
		System.out.println("--- Register ---");
		isConfirm=false;
		
		// Get first name with confirmation
		while (isConfirm==false){
			System.out.print("First Name:");
			firstName=read.nextLine().trim();
			isConfirm=tools.confirm(firstName); 
		}
		
		// Get last name with confirmation
		isConfirm=false;
		while (isConfirm==false){
			System.out.print("Last Name:");
			lastName=read.nextLine().trim();
			isConfirm=tools.confirm(lastName);
		}
		
		// Get username with confirmation
		isConfirm=false;
		while(isConfirm==false){
			System.out.print("User Name:");
			userName=read.nextLine().trim();
			isConfirm=tools.confirm(userName);
			userName=userName.toLowerCase();
		}
		
		// Get PIN with confirmation
		isConfirm=false;
		while (isConfirm==false){
			System.out.print("Pin (4 digits):");
			pin=read.nextLine().trim();
			isConfirm=tools.confirm(pin);
		}
		isConfirm=false;
		
		// Encrypt the PIN for security
		String encryptedPin = tools.encrypt(pin);

		// Try to connect to database and insert new user
		Connection conn = Database.connect();
		
		// Check if database connection worked
		if (conn == null) {
			System.out.println("Cannot connect to database. Registration failed.");
			System.out.println("Press ENTER to try again...");
			read.nextLine().trim();
			tools.clearScreen();
			startupPageCallBack.run();
			return;
		}

		// SQL query to insert new user
		String sql = "INSERT INTO users(firstname, lastname, username, pin) VALUES(?,?,?,?)";

		try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
			// Set all the user information in the query
			pstmt.setString(1, firstName);
			pstmt.setString(2, lastName);
			pstmt.setString(3, userName);
			pstmt.setString(4, encryptedPin);
			
			// Execute the insert
			pstmt.executeUpdate();
			
			System.out.println("User registered successfully!");
			System.out.println("Welcome " + firstName + " " + lastName + "!");
			System.out.println("Press ENTER to login with your new account...");
			read.nextLine().trim();
			
			tools.clearScreen();
			
			// After registration, go to login
			login(startupPageCallBack,homecallback);
			
		} 
		catch (SQLException e) {
			// Handle specific database errors
			if (e.getMessage().contains("UNIQUE constraint failed")) {
				System.out.println("Username '" + userName + "' is already taken.");
				System.out.println("Please choose a different username.");
			} else if (e.getMessage().contains("no such table")) {
				System.out.println("Database tables are missing.");
				System.out.println("This should not happen - system will try to fix it.");
			} else {
				System.out.println("Registration failed due to database error.");
			}
			
			System.out.println("Press ENTER to try again...");
			read.nextLine().trim();
			tools.clearScreen();
			startupPageCallBack.run();
			
		} finally {
			// Always close the database connection
			try {
				if (conn != null) conn.close();
			} catch (SQLException e) {
				System.out.println("Error closing database connection");
			}
		}
		
	}
	public static void login(Runnable startupPageCallBack,Runnable homecallback){
		System.out.println("--- Login ---");
		boolean recordFound=false; 
		isConfirm=false;
		
		// Get username with confirmation
		while(isConfirm==false){
			System.out.print("Username:  ");
			userName = read.nextLine().trim();
			isConfirm=tools.confirm(userName);
			userName=userName.toLowerCase();
		}
		
		// Get PIN with confirmation
		isConfirm=false;
		while(isConfirm==false){
			System.out.print("Pin:  ");
			pin = read.nextLine().trim();
			isConfirm=tools.confirm(pin);
		}
		
		// Encrypt the PIN to match what's in database
		String encryptedPin = tools.encrypt(pin);

		// Try to connect to database
		Connection conn = Database.connect();
		
		// Check if database connection worked
		if (conn == null) {
			System.out.println("Cannot connect to database. Login failed.");
			System.out.println("Press ENTER to try again...");
			read.nextLine().trim();
			tools.clearScreen();
			startupPageCallBack.run();
			return;
		}

		// SQL query to check login credentials
		String sql = "SELECT * FROM users WHERE username = ? AND pin = ?";
		
		try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
			
			// Set username and PIN in the query
			pstmt.setString(1, userName);
			pstmt.setString(2, encryptedPin);
			
			// Execute the query
			ResultSet rs = pstmt.executeQuery();

			// Check if we found a matching user
			if (rs.next()) {
				// Login successful - get user's first name for welcome message
				userFirstName = rs.getString("firstname");
				userLastName = rs.getString("lastname");
				userUserName= rs.getString("username");
				
				System.out.println("Login successful!");
				System.out.println("Welcome back " + userFirstName + " " + userLastName + "!");
				System.out.println("Press ENTER to continue...");
				read.nextLine().trim();
				
				tools.clearScreen();
				homecallback.run(); // Go to main application
				
			} else {
				// Login failed - wrong username or PIN
				System.out.println("Login failed! Username or PIN incorrect.");
				System.out.println("Press ENTER to try registration instead...");
				read.nextLine().trim();
				
				tools.clearScreen();
				startupPageCallBack.run();
			}

		} catch (SQLException e) {
			// Handle database errors
			if (e.getMessage().contains("no such table")) {
				System.out.println("Database tables not found.");
				System.out.println("System will create them automatically.");
				System.out.println("Please try registration first to create tables.");
			} else {
				System.out.println("Login error occurred: " + e.getMessage());
			}
			
			System.out.println("Press ENTER to try registration...");
			read.nextLine().trim();
			
			tools.clearScreen();
			startupPageCallBack.run();
			
		} finally {
			// Always close the database connection
			try {
				if (conn != null) conn.close();
			} catch (SQLException e) {
				System.out.println("Error closing database connection");
			}
		}
	}
}