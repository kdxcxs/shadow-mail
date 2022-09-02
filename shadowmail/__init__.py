from flask import Flask
from sqlalchemy.exc import IntegrityError
from jinja2 import FileSystemLoader
import os

from shadowmail.models import db, Message
from shadowmail.views import views
from shadowmail.utils import inotify, maildir

def create_app():
    app = Flask(__name__)

    with app.app_context():
        theme_loader = TemplateLoader(
            os.path.join(app.root_path, "templates"), followlinks=True
        )
        app.jinja_loader = theme_loader

        app.config.from_object('shadowmail.config.Config')
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_PATH']
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        db.create_all()

        app.register_blueprint(views)

    def handle_mailbox(type_names, path, filename):
        if('IN_MOVED_TO' in type_names and '.mail,' in filename):
            msg = maildir.load_from_file(f'{path}/{filename}')
            with app.app_context():
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
        else:
            pass

    inotify.watch(app.config['MAILDIR'], handle_mailbox)

    return app

class TemplateLoader(FileSystemLoader):
    def __init__(self, searchpath, encoding="utf-8", followlinks=False):
        super(TemplateLoader, self).__init__(searchpath, encoding, followlinks)
        self.overriden_templates = {}

    def get_source(self, environment, template):
        template = "/" + template
        return super(TemplateLoader, self).get_source(environment, template)
