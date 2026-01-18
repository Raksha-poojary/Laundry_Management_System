import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess
from werkzeug.utils import secure_filename
import hashlib

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def run_c_program(args):
    exe = os.path.join(os.path.dirname(__file__), 'a.exe')  # Changed to a.exe
    if not os.path.exists(exe):
        return 'Backend executable not found.'
    try:
        result = subprocess.run(["./a"] + args, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f'Error running backend: {e}'

# User data file for simple authentication
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.txt')

def ensure_static_dir():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            pass
    with open(USERS_FILE, 'r') as f:
        for line in f:
            u, _ = line.strip().split(':', 1)
            if u == username:
                return False
    with open(USERS_FILE, 'a') as f:
        f.write(f'{username}:{hash_password(password)}\n')
    return True

def authenticate_user(username, password):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r') as f:
        for line in f:
            u, p = line.strip().split(':', 1)
            if u == username and p == hash_password(password):
                return True
    return False

def parse_closet_output(output):
    closet = []
    for line in output.splitlines():
        if line:
            parts = line.split(',')
            while len(parts) < 7:
                parts.append('')
            closet.append({
                'name': parts[0],
                'category': parts[1],
                'is_missing': parts[2] == '1',
                'in_laundry': parts[3] == '1',
                'lost_date': parts[4],
                'image': parts[5],
                'last_washed': parts[6]
            })
    return closet

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    laundry_days_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You may want to save laundry_day1 and laundry_day2 as well
        if register_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Username already exists!')
    return render_template('signup.html', laundry_days_list=laundry_days_list)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/closet', methods=['GET', 'POST'])
def closet():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    ensure_static_dir()
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        image_file = request.files.get('image')
        image_filename = "None"
        if image_file and image_file.filename:
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join('static', image_filename)
            image_file.save(image_path)
        result = run_c_program([username, 'add_cloth', name, category, image_filename])
        if "already exists" in result:
            flash('Duplicate cloth!')
        elif "Backend executable not found" in result or result.startswith('Error running backend'):
            flash(result)
        else:
            flash('Cloth added!')
        return redirect(url_for('closet'))
    output = run_c_program([username, 'list_clothes'])
    closet = parse_closet_output(output)
    categories_output = run_c_program([username, 'list_categories'])
    categories = [cat for cat in categories_output.splitlines() if cat]
    return render_template('closet.html', closet=closet, categories=categories)

@app.route('/delete_cloth/<name>/<category>')
def delete_cloth(name, category):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    run_c_program([username, 'delete_cloth', name, category])
    flash('Cloth deleted!')
    return redirect(url_for('closet'))

@app.route('/mark_missing/<name>/<category>')
def mark_missing(name, category):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    run_c_program([username, 'mark_missing', name, category])
    flash('Cloth marked as missing!')
    return redirect(url_for('closet'))

@app.route('/mark_received/<name>/<category>')
def mark_received(name, category):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    run_c_program([username, 'mark_received', name, category])
    flash('Cloth marked as received!')
    return redirect(url_for('closet'))

@app.route('/send_laundry', methods=['GET', 'POST'])
def send_laundry():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if request.method == 'POST':
        selected = request.form.getlist('clothes')
        for item in selected:
            name, category = item.split('|')
            run_c_program([username, 'send_laundry', name, category])
        flash('Laundry sent!')
        return redirect(url_for('closet'))
    output = run_c_program([username, 'list_available_for_laundry'])
    closet = parse_closet_output(output)
    categories = sorted(set(cloth['category'] for cloth in closet if cloth['category'] and cloth['category'] != 'Never'))
    closet_by_category = {cat: [] for cat in categories}
    for cloth in closet:
        if cloth['category'] in closet_by_category:
            closet_by_category[cloth['category']].append(cloth)
    return render_template('send_laundry.html', closet_by_category=closet_by_category, categories=categories)

@app.route('/mark_received_laundry/<name>/<category>')
def mark_received_laundry(name, category):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    run_c_program([username, 'return_laundry', name, category])
    flash('Cloth marked as received from laundry!')
    return redirect(url_for('closet'))

@app.route('/mark_missing_laundry/<name>/<category>')
def mark_missing_laundry(name, category):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    run_c_program([username, 'mark_missing', name, category])
    flash('Cloth marked as missing from laundry!')
    return redirect(url_for('closet'))

@app.route('/laundry_management')
def laundry_management():
    return redirect(url_for('closet'))

@app.route('/laundry')
def laundry():
    if 'username' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('send_laundry')) 

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
