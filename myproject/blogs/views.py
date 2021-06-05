from myproject import db
from flask import render_template, request, redirect, Blueprint, flash, url_for, abort
from flask_login import current_user, login_required
from myproject.models import Blog, Comment
from myproject.blogs.forms import BlogPostForm


blogs_blueprint = Blueprint('blogs', __name__, template_folder='templates/blogs')


# Create
@blogs_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post = Blog(
            title=form.title.data,
            text=form.text.data,
            user_id=current_user.id
        )
        db.session.add(blog_post)
        db.session.commit()
        flash('Blog Post Created!')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)


# View Blog
@blogs_blueprint.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post_query = Blog.query.get_or_404(blog_post_id)
    comments = Comment.query.filter_by(blog_id=blog_post_id).all()
    return render_template('blog_post.html',
                           title=blog_post_query.title,
                           date=blog_post_query.date,
                           post=blog_post_query,
                           comments=comments)


# Update
@blogs_blueprint.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(blog_post_id):
    blog_post = Blog.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data

        db.session.commit()  # Just update no need to add!
        flash('Blog Post Updated!')
        return redirect(url_for('blogs.blog_post', blog_post_id=blog_post.id))
        # We provided needed id in url by passing parameter with redirect
    elif request.method == 'GET':
        form.text.data = blog_post.text
        form.title.data = blog_post.title

    return render_template('create_post.html', title='Updating', form=form)


# Delete
@blogs_blueprint.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = Blog.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)

    db.session.delete(blog_post)
    db.session.commit()
    flash('Blog Post Deleted!')
    return redirect(url_for('core.index'))
