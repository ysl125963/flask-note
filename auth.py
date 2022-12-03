from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import User
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('登录成功!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('密码错误!', category='error')
        else:
            flash('该邮箱尚未注册!', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        regex = re.compile(r'([A-Za-z\d]+[.-_])*[A-Za-z\d]+@[A-Za-z\d]+(\.[A-Z|a-z]{2,})+')
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash(message='该邮箱已被注册!', category='error')
        elif not re.fullmatch(regex, email):
            flash(message='请输入正确的邮箱!', category='error')
        elif len(username) < 4:
            flash(message='用户名不得少于4个字符!', category='error')
        elif len(password1) < 7:
            flash(message='密码不得少于7个字符!', category='error')
        elif password1 != password2:
            flash(message='两次输入的密码不一致!', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash(message='注册成功', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)

