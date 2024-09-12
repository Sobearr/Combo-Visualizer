from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from combovis.app import db
from .forms import LoginForm, RegisterForm
from .models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


# Route that handles user log in
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Prevent logged users to access the login page
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    # login logic
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('core.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


# Route that handles user registration
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Prevent logged users to access the register page
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))

    # Register logic
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))

        # Add user to DB
        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration sucessful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


# Route that handles user log out
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))
