from flask import g
from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from logic.user.application.port.incoming.ProfileUseCase import ProfileQueryUseCase, ProfileUpdateUseCase, ProfileDeleteUseCase
from src.user_container import UserContainer
from app.util import validator
from flask import request

profile_ns = Namespace('profile', description='프로필')


user_model = profile_ns.model('유저 모델', {
    '_id': fields.Integer(description='유저 ID', example=1674995732373),
    'name': fields.String(description='이름', example='김개발'),
    'username': fields.String(description='아이디', example='milcampus1234'),
    'nickname': fields.String(description='닉네임', example='개발이'),
    'account_number': fields.String(description='계좌번호', example='123-1234-123456 농협'),
    'email': fields.String(description='이메일', example='milcampus1234@naver.com')
})


@profile_ns.route('')
class Profile(Resource):
    @profile_ns.doc(security='jwt', description='유저 정보를 반환합니다')
    @profile_ns.marshal_with(code=200, description='조회 성공', fields=user_model, mask=None)
    @inject
    def get(self, profile_use_case: ProfileQueryUseCase = Provide[UserContainer.profile_query_service]):
        """유저 정보"""
        user = profile_use_case.get(g.id)
        return user.json

    @profile_ns.doc(security='jwt', description='회원탈퇴')
    @profile_ns.response(code=204, description='탈퇴 성공')
    @inject
    def delete(self, profile_use_case: ProfileDeleteUseCase = Provide[UserContainer.profile_delete_service]):
        """회원탈퇴"""
        profile_use_case.delete(g.id)
        return '', 204


@profile_ns.route('/password')
class ModifyPassword(Resource):
    @profile_ns.doc(security='jwt', description='신규 비밀번호로 변경합니다')
    @profile_ns.expect(profile_ns.model('비밀번호 변경', {
        'current_password': fields.String(description='현재 비밀번호', example='currentPassword4321'),
        'new_password': fields.String(description='신규 비밀번호', example='newPassword4321')
    }))
    @profile_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, profile_use_case: ProfileUpdateUseCase = Provide[UserContainer.profile_update_service]):
        """비밀번호 변경"""
        data = request.get_json()
        current_password = data['current_password']
        new_password = data['new_password']

        validator.validate_password(current_password)
        validator.validate_password(new_password)

        profile_use_case.update_password(g.id, current_password, new_password)
        return '', 204


@profile_ns.route('/nickname')
class ModifyNickname(Resource):
    @profile_ns.doc(security='jwt', description='닉네임을 변경합니다')
    @profile_ns.expect(profile_ns.model('닉네임 변경', {
        'nickname': fields.String(description='변경 닉네임', example='개발이여친')
    }))
    @profile_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, profile_use_case: ProfileUpdateUseCase = Provide[UserContainer.profile_update_service]):
        """닉네임 변경"""
        data = request.get_json()
        nickname = data['nickname']

        validator.validate_nickname(nickname)

        profile_use_case.update_nickname(g.id, nickname)
        return '', 204


@profile_ns.route('/account-number')
class ModifyAccountNumber(Resource):
    @profile_ns.doc(security='jwt', description='계좌번호를 변경합니다')
    @profile_ns.expect(profile_ns.model('계좌번호 변경', {
        'account_number': fields.String(description='변경 계좌번호', example='111-1111-1111-11 신한')
    }))
    @profile_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, profile_use_case: ProfileUpdateUseCase = Provide[UserContainer.profile_update_service]):
        """계좌번호 변경"""
        data = request.get_json()
        account_number = data['account_number']

        validator.validate_account_number(account_number)

        profile_use_case.update_account_number(g.id, account_number)
        return '', 204
