from flask import render_template, redirect, url_for, Blueprint, flash, abort, request
from flask_login import current_user, login_required
from myproject import db
from myproject.models import Message, User
from myproject.mail.forms import MessageForm
from sqlalchemy import and_


messages_blueprint = Blueprint('messages', __name__, template_folder='templates/mail')


@messages_blueprint.route('/inbox')
@login_required
def inbox():
    messages = Message.query.filter(and_(Message.receiver_id == current_user.id,
                                    Message.MESSAGE_VISIBLE_TO.isnot(str(current_user.id)))).all()

    # Ako MESSAGE_VISIBLE_TO == current_user.id to znaci da je on vec kliknuo na DELETE MESSAGE!

    users = User.query.all()
    return render_template('inbox.html', messages=messages, users=users)


@messages_blueprint.route('/inbox_sent')
@login_required
def sent_messages():
    messages = Message.query.filter(and_(Message.sender_id == current_user.id,
                                    Message.MESSAGE_VISIBLE_TO.isnot(str(current_user.id)))).all()

    users = User.query.all()

    return render_template('inbox_sent_messages.html', messages=messages, users=users)


@messages_blueprint.route('/message_create', methods=['GET', 'POST'])
@login_required
def create_message():
    form = MessageForm()
    if form.validate_on_submit():
        receiver = User.query.filter_by(username=form.receiver.data.lower()).first()
        message = Message(
            title=form.title.data,
            text=form.text.data,
            sender_id=current_user.id,
            receiver_id=receiver.id
        )
        db.session.add(message)
        db.session.commit()
        flash('Message Sent!')
        return redirect(url_for('messages.inbox'))
    return render_template('create_message.html', form=form)


@messages_blueprint.route('/view_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    message.seen = True
    db.session.commit()
    return render_template('message.html', message=message)


@messages_blueprint.route('/delete_inbox_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def delete_inbox_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.receiver_id != current_user.id:
        abort(403)

    if message.MESSAGE_VISIBLE_TO is not None:
        db.session.delete(message)
        db.session.commit()
    else:
        message.MESSAGE_VISIBLE_TO = message.receiver_id
        db.session.commit()
    return redirect(url_for('messages.inbox'))


@messages_blueprint.route('/delete_sent_message/<int:message_id>', methods=['GET', 'POST'])
@login_required
def delete_sent_message(message_id):
    message = Message.query.get_or_404(message_id)
    if message.sender_id != current_user.id:
        abort(403)

    if message.MESSAGE_VISIBLE_TO is not None:
        db.session.delete(message)
        db.session.commit()
    else:
        message.MESSAGE_VISIBLE_TO = message.sender_id
        db.session.commit()
    return redirect(url_for('messages.sent_messages'))


