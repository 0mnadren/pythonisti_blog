from flask import render_template, redirect, url_for, Blueprint, flash, abort
from flask_login import current_user, login_required
from myproject import db
from myproject.models import Message, User
from myproject.mail.forms import MessageForm


messages_blueprint = Blueprint('messages', __name__, template_folder='templates/mail')


@messages_blueprint.route('/inbox')
@login_required
def inbox():
    print(Message.query.all())
    messages = Message.query.filter_by(receiver_id=current_user.id).all()
    return render_template('inbox.html', messages=messages)


@messages_blueprint.route('/inbox_sent')
@login_required
def sent_messages():
    messages = Message.query.filter_by(sender_id=current_user.id).all()
    return render_template('inbox_sent_messages.html', messages=messages)


@messages_blueprint.route('/message_create', methods=['GET', 'POST'])
@login_required
def create_message():
    form = MessageForm()
    form.receiver.choices = [(user.id, user.username) for user in User.query.all() if user.id != current_user.id]
    if form.validate_on_submit():
        message = Message(
            title=form.title.data,
            text=form.text.data,
            sender_id=current_user.id,
            receiver_id=form.receiver.data
        )
        db.session.add(message)
        db.session.commit()
        print(form.receiver.data)
        flash('Message Sent!')
        return redirect(url_for('messages.inbox'))
    return render_template('create_message.html', form=form)


@messages_blueprint.route('/view_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    return render_template('message.html', message=message)


@messages_blueprint.route('/delete_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.receiver_id != current_user.id:
        abort(403)

    db.session.delete(message)
    db.session.commit()
    flash('Message deleted!')
    return redirect(url_for('messages.inbox'))


