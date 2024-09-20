from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from webapp.common.database import engine

from webapp.domain.auth.persistance.token_repository import TokenRepository
from webapp.domain.auth.persistance.kakao_repository import KakaoRepository
from webapp.domain.auth.application.jwt_auth_service import JWTAuthService
from webapp.domain.auth.application.kakao_auth_service import KakaoAuthService

from webapp.domain.user.persistance.user_repository import UserRepository
from webapp.domain.user.application.user_service import UserService

from webapp.domain.taxi_group.application.taxi_group_service import TaxiGroupService
from webapp.domain.taxi_group.persistance.taxi_group_repository import TaxiGroupRepository
from webapp.domain.taxi_group.application.query_service import QueryService
from webapp.domain.taxi_group.persistance.taxi_group_dao import TaxiGroupDao


def get_session():
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        if session.dirty or session.new or session.deleted:
            session.commit()
        session.close()


def get_kakao_repository(session=Depends(get_session)):
    return KakaoRepository(session=session)


def get_token_repository(session=Depends(get_session)):
    return TokenRepository(session=session)


def get_user_repository(session=Depends(get_session)):
    return UserRepository(session=session)


def get_taxi_group_repository(session=Depends(get_session)):
    return TaxiGroupRepository(session=session)


def get_taxi_group_dao(session=Depends(get_session)):
    return TaxiGroupDao(session=session)


def get_user_service(user_repository=Depends(get_user_repository)):
    return UserService(user_repository=user_repository)


def get_jwt_auth_service(token_repository=Depends(get_token_repository)):
    return JWTAuthService(token_repository=token_repository)


def get_kakao_auth_service(
        user_service=Depends(get_user_service),
        jwt_auth_service=Depends(get_jwt_auth_service),
        kakao_repository=Depends(get_kakao_repository)
):
    return KakaoAuthService(
        user_service=user_service,
        jwt_auth_service=jwt_auth_service,
        kakao_repository=kakao_repository
    )


def get_taxi_group_service(taxi_group_repository=Depends(get_taxi_group_repository)):
    return TaxiGroupService(taxi_group_repository=taxi_group_repository)


def get_query_service(taxi_group_dao=Depends(get_taxi_group_dao)):
    return QueryService(taxi_group_dao=taxi_group_dao)
