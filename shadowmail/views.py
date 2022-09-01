from flask import current_app as app
from flask import Blueprint, render_template
from sqlalchemy.exc import IntegrityError

from shadowmail.models import db, Message
from shadowmail.utils import maildir

views = Blueprint("views", __name__)

@views.route('/')
def index():
    msgs = Message.query.all()
    return render_template('index.html', msgs=msgs)

@views.route('/setup')
def setup():
    for msg in maildir.get_site_message(app.config['MAILDIR']):
        try:
            db.session.add(Message(
                msg_file = msg['filename'],
                msg_date= msg['date'],
                msg_subject= msg['subject'],
                msg_from= msg['from'],
                msg_to= msg['to'],
            ))
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            return render_template('setup.html', success=False)
    return render_template('setup.html', success=True)
