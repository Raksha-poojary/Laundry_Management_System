# Laundry Management System

A simple Laundry Management System written in C, with a basic web interface using Flask and HTML.

## Features
- Add, delete, and manage clothes for each user
- Track laundry status (sent, returned)
- Mark items as missing or received
- Simple web interface for user interaction
- All user data stored in `static/user.txt`

## How It Works
- Each user can log in and manage their own closet.
- All closet data for all users is stored in a single file (`static/user.txt`), with each line prefixed by the username.
- The C backend handles file operations and logic for managing clothes and laundry status.
- The Flask app provides a web interface for users to interact with the system.

## Getting Started
1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/Laundry_Management_System.git
   cd Laundry_Management_System
   ```
2. **Compile the C program:**
   ```
   gcc main.c -o laundry
   ```
3. **Run the Flask app:**
   ```
   python app.py
   ```
4. **Open your browser:**
   Go to `http://localhost:5000` to use the web interface.

## File Structure
- `main.c` - C source code for backend logic
- `app.py` - Flask web server
- `static/user.txt` - Stores all user closet data
- `templates/` - HTML templates for the web interface

## License
This project is for educational purposes.
<<<<<<< HEAD

=======
>>>>>>> 0d9c156 (Initial commit)
