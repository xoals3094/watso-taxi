from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from flask import request
from src.user_container import UserContainer
from app.util import validator
from logic.user.application.port.incoming.ForgotUseCase import ForgotUsernameUseCase, ForgotPasswordUseCase


forgot_ns = Namespace('forgot', description='찾기')


temp_password_model = forgot_ns.model('임시 비밀번호', {
    'username': fields.String(description='아이디', example="milcampus1234"),
    'email': fields.String(description='이메일', example='miryany1234@naver.com')
})

email_parser = forgot_ns.parser()
email_parser.add_argument('email', type=str, help='이메일')


@forgot_ns.route('/username')
class ForgotUsername(Resource):
    @forgot_ns.doc(description='이메일로 유저 아이디를 발송합니다', parser=email_parser)
    @forgot_ns.response(code=204, description='조회 성공')
    @inject
    def get(self, forgot_use_case: ForgotUsernameUseCase = Provide[UserContainer.forgot_username_service]):
        """아이디 찾기"""
        email = request.args['email']
        validator.validate_email(email)

        forgot_use_case.send_username_email(email)
        return '', 204


@forgot_ns.route('/password')
class ForgotPassword(Resource):
    @forgot_ns.doc(description='임시 비밀번호를 발급합니다', body=temp_password_model)
    @forgot_ns.response(code=204, description='발송 성공')
    @inject
    def post(self, forgot_use_case: ForgotPasswordUseCase = Provide[UserContainer.forgot_password_service]):
        """임시 비밀번호 발급"""
        data = request.get_json()

        username = data['username']
        email = data['email']

        validator.validate_username(username)
        validator.validate_email(email)

        forgot_use_case.send_temp_password(username, email)
        return '', 204
