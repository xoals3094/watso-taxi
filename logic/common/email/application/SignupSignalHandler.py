from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer

from logic.common.email.application.port.outgoing.EmailSender import EmailSender

from blinker import signal

signup_signal = signal('signup-signal')


@signup_signal.connect_via('auth_email')
@inject
def signup_auth_signal_handler(sender, email, auth_code,
                               email_sender: EmailSender = Provide[CommonContainer.email_sender]):
    subject = '[왔소] 회원가입 인증코드입니다.'
    body = f'인증코드 : {auth_code}'

    email_sender.send(email, subject, body)
