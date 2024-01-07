from dependency_injector.wiring import inject, Provide
from src.common_container import CommonContainer

from logic.common.email.application.port.outgoing.EmailSender import EmailSender

from blinker import signal

forgot_signal = signal('forgot-signal')


@forgot_signal.connect_via('temp-password')
@inject
def signup_auth_signal_handler(sender, temp_password, email,
                               email_sender: EmailSender = Provide[CommonContainer.email_sender]):

    subject = '[왔소] 임시 비밀번호입니다.'
    body = f'임시 비밀번호 : {temp_password}'

    email_sender.send(email, subject, body)


@forgot_signal.connect_via('username')
@inject
def signup_auth_signal_handler(sender, email, username,
                               email_sender: EmailSender = Provide[CommonContainer.email_sender]):

    subject = '[왔소] 아이디 찾기 결과입니다.'
    body = f'아이디 : {username}'

    email_sender.send(email, subject, body)