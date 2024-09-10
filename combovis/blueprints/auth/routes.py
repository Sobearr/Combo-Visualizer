from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from combovis.app import db
from .forms import LoginForm, RegisterForm
from .models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('core.index'))
        flash('Invalid username or password', 'danger')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('core.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Save user to db
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration sucessful!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@auth_bp.route('/restricted')
@login_required
def restricted():
    return render_template('auth/restricted.html')
