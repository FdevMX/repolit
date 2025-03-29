from flask import Blueprint, render_template, request, redirect, url_for, flash

login_view = Blueprint('login_view', __name__)

@login_view.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Here you would typically verify the username and password
        # For example, by checking against a database
        
        if username == 'admin' and password == 'password':  # Example check
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard_view.dashboard'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    
    return render_template('login.html')  # Ensure you have a login.html template in your templates directory