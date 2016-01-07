# -*- coding: utf-8 -*-
#! /usr/bin/env python

'''
send email via Django
'''

import sys, os

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('DJANGO_PROJECT_PATH')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.conf import settings
from django.core.mail import EmailMessage

def mail_report(mail_subject, filename, mail_user):
   email = EmailMessage(mail_subject,'',settings.EMAIL_HOST_USER,to=[mail_user])
   email.attach_file(filename)
   email.send()
   
if __name__ == '__main__':
   mail_report("test", "/path/attachment", "sample@user.com")

