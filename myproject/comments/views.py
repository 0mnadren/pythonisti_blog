from myproject import db
from flask_login import current_user, login_required
from flask import redirect, render_template, url_for, Blueprint, abort, request, flash
from myproject.models import Comment
from .forms import CommentForm

comments_blueprint = Blueprint('comments', __name__)


# Create
@comments_blueprint.route('/<blog_post_id>/create_comment', methods=['GET', 'POST'])
@login_required
def create_comment(blog_post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            text=form.text.data,
            user_id=current_user.id,
            blog_id=blog_post_id
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blogs.blog_post', blog_post_id=blog_post_id))
    return render_template('create_comment.html', form=form)


@comments_blueprint.route('/comment/<comment_id>', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.comment_author != current_user:
        abort(403)

    form = CommentForm()
    if form.validate_on_submit():
        comment.text = form.text.data
        db.session.commit()
        return redirect(url_for('blogs.blog_post', blog_post_id=comment.blog_id))
    elif request.method == 'GET':
        form.text.data = comment.text

    return render_template('create_comment.html', form=form)


@comments_blueprint.route('/comment/<comment_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.comment_author != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!')
    return redirect(url_for('blogs.blog_post', blog_post_id=comment.blog_id))
