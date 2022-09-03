from flask import current_app as app
from flask import Blueprint, render_template, request, session, redirect
from sqlalchemy.exc import IntegrityError

from shadowmail.models import db, Message, Shadow
from shadowmail.utils import maildir, shadow_manage

views = Blueprint("views", __name__)

@views.route('/')
def index():
    msgs = Message.query.order_by(Message.msg_date.desc()).all()
    shads = Shadow.query.count()
    return render_template('index.html', msgs=msgs, shads=shads)

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

@views.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        app.logger.info(app.config['ACCESS_TOKEN'])
        app.logger.info(request.form['token'])
        if request.form['token'] == app.config['ACCESS_TOKEN']:
            session['auth'] = True
            return redirect('/', 302)
        else:
            return render_template('auth.html', wrong=True)
    return render_template('auth.html')

@views.route('/preview')
def preview():
    msg = Message.query.filter_by(id=int(request.args['id'])).first()
    return msg.msg_text if msg.msg_html == '' else msg.msg_html

@views.route('/shadow', methods=['POST'])
def shadow():
    email = request.form['email']
    password = request.form['password']
    try:
        db.session.add(Shadow(
            email = email,
            password = password,
        ))
        db.session.commit()
        shadow_manage.add_shadow(email, password)
    except IntegrityError as e:
        db.session.rollback()
        return render_template('shadow.html', success=False, shadow=email)
    return render_template('shadow.html', success=True, shadow=email)
