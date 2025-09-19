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