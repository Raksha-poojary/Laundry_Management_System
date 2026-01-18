# Laundry Management System

A simple Laundry Management System built with C and a Flask web interface. This project allows users to manage their clothes, track laundry status, and handle lost or missing items. All user data is stored in a single file for easy management.

## Features

- User registration and login
- Add, delete, and manage clothes
- Track laundry status (sent, returned)
- Mark items as missing or received
- Simple, modern web interface (Bootstrap)
- All user data stored in `static/user.txt`

## Folder Structure

```
Laundry_Management_System/
│
├── main.c                  # Core C logic for laundry management
├── app.py                  # Flask app for web interface
├── static/
│   └── user.txt            # Stores all users' closet data
├── templates/
│   ├── home.html           # Landing page
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
│   ├── dashboard.html      # User dashboard
│   ├── closet.html         # Closet management
│   ├── laundry.html        # Laundry status
│   └── send_laundry.html   # Send laundry form
└── README.md               # Project documentation
```

## Getting Started

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/Laundry_Management_System.git
   cd Laundry_Management_System
   ```

2. **Compile the C code:**
   ```
   gcc main.c -o laundry
   ```

3. **Run the Flask app:**
   ```
   python app.py
   ```

4. **Open your browser:**  
   Go to `http://127.0.0.1:5000/` to use the web interface.

## Requirements

- Python 3.x
- Flask (`pip install flask`)
- GCC (for compiling C code)

## License

This project is for educational purposes.

---
