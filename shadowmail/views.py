from flask import current_app as app
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError

from shadowmail.models import db, Message
from shadowmail.utils import maildir

views = Blueprint("views", __name__)

@views.route('/')
def index():
    msgs = Message.query.order_by(Message.msg_date.desc()).all()
    return render_template('index.html', msgs=msgs)

@views.route('/setup')
def setup():
    for msg in maildir.get_site_message(app.config['MAILDIR']):
        try:
            db.session.add(Message(
                msg_filename = msg.filename,
                msg_date = msg.parsedmail.date,
                msg_subject = msg.parsedmail.subject,
                msg_from_name = msg.parsedmail.from_[0][0],
                msg_from_addr = msg.parsedmail.from_[0][1],
                msg_to_name = msg.parsedmail.to[0][0],
                msg_to_addr = msg.parsedmail.to[0][1],
                msg_text = '\n'.join(msg.parsedmail.text_plain),
                msg_html = '\n'.join(msg.parsedmail.text_html),
            ))
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return render_template('setup.html', success=False)
    return render_template('setup.html', success=True)
