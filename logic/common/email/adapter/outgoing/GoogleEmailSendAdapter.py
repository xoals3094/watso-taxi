import smtplib
from email.mime.text import MIMEText
from multiprocessing import Process
from config.production.email import sender_email, code
from logic.common.email.application.port.outgoing.EmailSender import EmailSender


class EmailProcess(Process):
    def __init__(self, from_email, to_email, subject, body):
        self.from_email = from_email
        self.to_email = to_email
        self.subject = subject
        self.body = body
        Process.__init__(self)

    def run(self):
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login(self.from_email, code)

        msg = MIMEText(self.body)
        msg['Subject'] = self.subject

        smtp.sendmail(self.from_email, self.to_email, msg.as_string())
        smtp.quit()


class GoogleEmailSender(EmailSender):
    def __init__(self):
        self.from_email = sender_email
        self.app_code = code

    def send(self, to, subject, body):
        EmailProcess(self.from_email, to, subject, body).start()
