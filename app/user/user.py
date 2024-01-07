from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from logic.user.application.port.incoming.UserUseCase import UserUseCase
from src.user_container import UserContainer
from flask import request

duplicate_check_ns = Namespace('user', description='유저')

duplicate_result_model = duplicate_check_ns.model("중복 여부", {
    'is_duplicated': fields.Boolean(description="중복 여부")
})

parser = duplicate_check_ns.parser()
parser.add_argument('field', type=str, help='중복을 검사할 필드', choices=('username', 'nickname', 'email'))
parser.add_argument('value', type=str, help='중복을 검사할 값')


@duplicate_check_ns.route('')
class UsernameCheck(Resource):
    @duplicate_check_ns.doc(parser=parser, description="필드의 값이 중복되는지 검사합니다")
    @duplicate_check_ns.response(code=200, description="검사 결과", model=duplicate_result_model)
    @inject
    def get(self, user_use_case: UserUseCase = Provide[UserContainer.user_service]):
        """중복체크"""
        is_duplicated = user_use_case.check_exist_user(request.args['field'], request.args['value'])

        return {'is_duplicated': is_duplicated}
