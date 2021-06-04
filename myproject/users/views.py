from flask import render_template, redirect, url_for, flash, request, Blueprint, abort
from flask_login import login_required, login_user, current_user, logout_user
from myproject import db
from myproject.models import User, Blog
from myproject.users.forms import LoginForm, RegisterForm, UpdateUserForm
from myproject.users.picture_handler import add_profile_pic


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out!')
    return redirect(url_for('core.index'))


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Thank you for registration!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                flash('Login Success!')

                next = request.args.get('next')
                if next is None or not next[0] == '/':
                    next = url_for('core.index')

                return redirect(next)
    return render_template('login.html', form=form)


@users_blueprint.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:  # If user uploaded pic
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users_blueprint.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
    user = User.query.get_or_404(current_user.id)
    if user.id != current_user.id:
        abort(403)
    db.session.delete(user)
    db.session.commit()
    flash('Account has been deleted!')
    return redirect(url_for('core.index'))


@users_blueprint.route('/<username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)  # Important for pagination
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = Blog.query.filter_by(author=user).order_by(Blog.date.desc()).paginate(page=page,
                                                                                       per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)


