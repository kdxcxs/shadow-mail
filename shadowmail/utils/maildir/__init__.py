"""Handles stuffs relatied to maildir"""

import email
import os, mailbox, time, datetime

class ParsedMessage():
    def __init__(self, filename, email_msg):
        self.data = {}
        self.data['filename'] = filename
        self.data['date']     = datetime.datetime.fromtimestamp(time.mktime(time.strptime(email_msg['date'], '%a, %d %b %Y %H:%M:%S %z')))
        self.data['subject']  = email_msg['subject']
        self.data['from']     = email_msg['from'].split(' ')[-1]
        self.data['to']       = email_msg['to'].split(' ')[-1]
        self.data['payload']  = email_msg.get_payload()[0].get_payload(decode = True).decode(email_msg.get_charsets()[1])
    def __getitem__(self, name):
        return self.data[name]

def load_from_file(path):
    msg = None
    with open(path) as f:
        msg = ParsedMessage(path.split('/')[-1].split(':')[0], email.message_from_file(f))
    return msg

def get_domain_messages(maildir_path):
    messages = []
    for shadow in os.listdir(maildir_path): # Each email account is a shadow
        box = mailbox.Maildir(f'{maildir_path}/{shadow}')
        messages.extend([ParsedMessage(*m) for m in box.items()])
    return messages

def get_site_message(maildir_path):
    return [msg for domain in os.listdir(maildir_path) if os.path.isdir(f'{maildir_path}/{domain}') for msg in get_domain_messages(f'{maildir_path}/{domain}')]
