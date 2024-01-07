from flask import request
from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from app.util import validator

from logic.user.application.port.incoming.SignupUseCase import SignupUseCase, SignupAuthUseCase
from logic.user.dto.presentaition import SignupModel

signup_ns = Namespace('signup', description='회원가입')


signup_format_model = signup_ns.model('회원가입', {
    'auth_token': fields.String(description='인증 토큰', example='jwt'),
    'name': fields.String(description='이름', required=True, example='김개발'),
    'username': fields.String(description='유저 ID', required=True, example='milcampus1234'),
    'pw': fields.String(description='비밀번호', required=True, example='dogLegBirdLeg1234'),
    'nickname': fields.String(description='닉네임', required=True, example='개발이'),
    'account_number': fields.String(description='계좌번호', required=True, example='123-1234-123456 농협'),
    'email': fields.String(description='이메일', required=True, example='milcampus1234@naver.com')
})

email_parser = signup_ns.parser()
email_parser.add_argument('email', type=str, help='이메일')


@signup_ns.route('')
class Signup(Resource):
    @signup_ns.doc(parser=email_parser, description="이메일에 인증코드를 발송합니다")
    @signup_ns.response(code=204, description='요청 성공')
    @inject
    def get(self, signup_use_case: SignupAuthUseCase = Provide[UserContainer.signup_auth_service]):
        """회원가입 인증코드 발송"""
        email = request.args['email']

        validator.validate_email(email)

        signup_use_case.send_auth_email(email)
        return '', 204

    @signup_ns.doc(description="회원가입")
    @signup_ns.expect(signup_format_model)
    @signup_ns.response(code=201, description='가입 성공')
    @inject
    def post(self, signup_use_case: SignupUseCase = Provide[UserContainer.signup_service]):
        """회원가입"""
        data = request.get_json()
        signup_model = SignupModel(**data)
        signup_use_case.signup(signup_model)

        return '', 201


validation_parser = signup_ns.parser()
validation_parser.add_argument('auth-code', type=str, help='인증코드')
validation_parser.add_argument('email', type=str, help='이메일')


@signup_ns.route('/validation-check')
class SignupValidation(Resource):
    @signup_ns.doc(parser=validation_parser, description="인증코드의 유효성을 검사 후 인증 토큰을 발급합니다")
    @signup_ns.response(code=200, description='인증 성공', model=signup_ns.model('인증성공', {
        'auth_token': fields.String(description='인증을 성공적으로 완수했음을 증명해주는 토큰', example='jwt')
    }))
    @inject
    def get(self, signup_use_case: SignupAuthUseCase = Provide[UserContainer.signup_auth_service]):
        """인증코드 유효성 검사"""
        auth_code = request.args['auth-code']
        email = request.args['email']

        validator.validate_auth_code(auth_code)
        validator.validate_email(email)

        auth_token = signup_use_case.validate_auth_code(email, auth_code)
        return {'auth_token': auth_token}, 200
