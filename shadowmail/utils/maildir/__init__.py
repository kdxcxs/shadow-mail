"""Handles stuffs relatied to maildir"""

import os, mailbox, mailparser

class ParsedMail(object):
    def __init__(self, filename, parsedmail):
        self._filename = filename.split(':')[0]
        self._parsedmail = parsedmail
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def parsedmail(self):
        return self._parsedmail

def load_from_file(path):
    return ParsedMail(path.split('/')[-1], mailparser.parse_from_file(path))

def get_domain_messages(maildir_path):
    messages = []
    for shadow in [s for s in os.listdir(maildir_path) if os.path.isdir(f'{maildir_path}/{s}/cur')]: # Each email account is a shadow
        box = mailbox.Maildir(f'{maildir_path}/{shadow}')
        messages.extend([ParsedMail(m[0], mailparser.parse_from_string(m[1].as_string())) for m in box.items()])
    return messages

def get_site_message(maildir_path):
    return [msg for domain in os.listdir(maildir_path) if os.path.isdir(f'{maildir_path}/{domain}') for msg in get_domain_messages(f'{maildir_path}/{domain}')]
