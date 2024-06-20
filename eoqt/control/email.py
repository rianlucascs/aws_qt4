from control import account
from email.message import EmailMessage
from control.utils import date_today, read_file
from sys import path
import smtplib
import ssl
from control.straton import StratOn
from os import listdir
import mimetypes
from os.path import basename
from control.log import LogQt

class Email:

    def __init__(self):
        self._origin = account.email
        self._fate = account.email
        self._password = account.password

    def _get_log_and_transformer(self):
        file = read_file(f'{path[0]}\\logs\\executionHistory.txt').split('\n')
        content = f'# EXECUTION LOGS FOR THE DAY {date_today()}\n\n'
        for row in file:
            if row[2:12] == date_today():
                content += f'{row}\n'
        return content
    
    def add_message(self, email, message):
        return email.set_content(message)

    def _create_message_pdf(self, path_, email, file):
        if '.pdf' in file:
            path_file = f'{path_}\\{file}'
            mime_type, mime_subtype = mimetypes.guess_type(path_file)[0].split('/')
            with open(path_file, 'rb') as ap:
                email.add_attachment(ap.read(), maintype=mime_type,
                                    subtype=mime_subtype, filename=basename(path_file))
            
    def _get_pdfs_control(self, email):
        path_control = f'{path[0]}\\control'
        for file in listdir(path_control):
            self._create_message_pdf(path_control, email, file)
      
    def _get_pdfs_strats(self, email):
        for path_strat in StratOn().paths_strategies():
            for file in listdir(path_strat):
                self._create_message_pdf(path_strat, email, file)

    def send(self):
        email = EmailMessage()

        email['From'] = self._origin
        email['To'] = self._fate
        email['Subject'] = f'{date_today()} AWS-QT4 REPORTS'

        self.add_message(email, self._get_log_and_transformer())
        safe = ssl.create_default_context()

        self._get_pdfs_control(email)
        self._get_pdfs_strats(email)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=safe) as smtp:
            smtp.login(self._origin, self._password)
            smtp.sendmail(self._origin, self._fate, email.as_string())

        LogQt('Email send').startup
