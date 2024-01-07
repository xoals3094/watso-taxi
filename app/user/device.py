from flask_restx import Resource, Namespace, fields
from dependency_injector.wiring import inject, Provide
from src.user_container import UserContainer
from flask import request
from logic.user.application.port.incoming.DeviceUseCase import DeviceUseCase


device_ns = Namespace('device', description='기기 관리')

notification_allow = device_ns.model('알림 허용', {
    'allow': fields.Boolean(description='허용여부'),
})


@device_ns.route('/token')
class Token(Resource):
    @device_ns.doc(security='jwt', description='기기 토큰 정보를 수정합니다.', body=device_ns.model('device', model={
        'device_token': fields.String(description='기기 토큰')
    }))
    @device_ns.response(code=204, description='추가 성공')
    @inject
    def patch(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """기기 토큰 수정 """
        access_token = request.headers['Authorization']
        data = request.get_json()
        device_use_case.update_device_token(access_token, data['device_token'])
        return '', 204


@device_ns.route('/notification')
class Notification(Resource):
    @device_ns.doc(security='jwt', description='알림 허용 상태를 조회합니다')
    @device_ns.response(code=200, description='조회 성공', model=notification_allow)
    @inject
    def get(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """알림 허용 상태 조회"""
        access_token = request.headers['Authorization']
        allow = device_use_case.get_notification_allow(access_token)
        return {'allow': allow}

    @device_ns.doc(security='jwt', description='알림 허용 상태를 변경합니다', body=notification_allow)
    @device_ns.response(code=204, description='변경 성공')
    @inject
    def patch(self, device_use_case: DeviceUseCase = Provide[UserContainer.device_service]):
        """알림 허용 상태 변경"""
        access_token = request.headers['Authorization']
        data = request.get_json()
        device_use_case.update_notification_allow(access_token, data['allow'])
        return '', 204
