from app import app
from flask import render_template, redirect, url_for, request, flash
from app.database import database
from app.auth.auth import insert_user, check_user_credentials, load_user
from flask_login import login_user, current_user, logout_user
from app.auth.auth_forms import SingupForm, LoginForm

@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        flash("You need to log out before you can create a new account.")
        return redirect(url_for('home'))
    form = SingupForm()
    if form.validate_on_submit():
        insert_user(form.login.data, form.password.data)
        flash(f"Your account has been created!. You can now log in.", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.")
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = check_user_credentials(form.login.data, form.password.data)
        if user:
            login_user(user)
            flash(f'Successfully logged in as {current_user.user_name}.')
            return redirect(url_for("home"))
        else:
            flash('Login unsuccessfull. Please check username and password.', 'danger')
    return render_template('login.html', form=form, user=current_user)

@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have been logged out.")
    else:
        flash('You need to log in before you can log out')
    return redirect(url_for('home'))