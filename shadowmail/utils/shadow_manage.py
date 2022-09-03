from flask import current_app as app
import sha512_crypt

def add_shadow(shadow, passwd):
    cf = app.config['POSTFIX_ACCOUNTS'] # postfix-accounts.cf
    with open(cf, 'a') as f:
        f.write(f'{shadow}|{{SHA512-CRYPT}}{sha512_crypt.encrypt(passwd)}')
