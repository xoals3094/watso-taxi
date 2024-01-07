class BaseException(Exception):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    @property
    def json(self):
        return {
            'msg': self.msg,
            'code': self.code,
        }


class DatabaseError(BaseException):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistResource(DatabaseError):
    def __init__(self, msg='존재하지 않는 리소스입니다', code=2):
        super().__init__(msg=msg, code=code)


class DuplicateKeyError(DatabaseError):
    def __init__(self, msg='중복 키가 존재합니다', code=3):
        super().__init__(msg=msg, code=code)


class FormatError(BaseException):
    def __init__(self, msg='입력값이 유효하지 않습니다', code=4):
        super().__init__(msg=msg, code=code)


class DeviceNotFound(BaseException):
    def __init__(self, msg='기기 정보를 찾을 수 없습니다', code=6):
        super().__init__(msg=msg, code=code)


# domain Error
class DomainError(BaseException):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


# 인증 에러
class AuthError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class AccessDenied(AuthError):
    def __init__(self, msg='접근 권한이 없습니다', code=100):
        super().__init__(msg=msg, code=code)


class SigninFail(AuthError):
    def __init__(self, msg='아이디 혹은 비밀번호가 일치하지 않습니다', code=101):
        super().__init__(msg=msg, code=code)


class NotExistUser(AuthError):
    def __init__(self, msg='유저 데이터를 찾을 수 없습니다', code=102):
        super().__init__(msg=msg, code=code)


class DuplicateUser(SigninFail):
    def __init__(self, msg='중복 유저가 존재합니다.', code=103):
        super().__init__(msg=msg, code=code)


class PasswordMismatch(AuthError):
    def __init__(self, msg='비밀번호가 일치하지 않습니다', code=104):
        super().__init__(msg=msg, code=code)


class NotValidAuthCode(AuthError):
    def __init__(self, msg='유효하지 않은 인증코드입니다', code=105):
        super().__init__(msg=msg, code=code)


# 토큰 에러
class TokenError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistToken(TokenError):
    def __init__(self, msg='토큰 정보를 찾을 수 없습니다', code=200):
        super().__init__(msg=msg, code=code)


class ExpiredToken(TokenError):
    def __init__(self, msg='토큰이 만료되었습니다', code=201):
        super().__init__(msg=msg, code=code)


# Store
class StoreError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistStore(StoreError):
    def __init__(self, msg='가게 정보를 찾을 수 없습니다', code=300):
        super().__init__(msg=msg, code=code)


class NotExistMenu(StoreError):
    def __init__(self, msg='메뉴 정보를 찾을 수 없습니다', code=301):
        super().__init__(msg=msg, code=code)


# post
class PostError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistPost(PostError):
    def __init__(self, msg='게시글 정보를 찾을 수 없습니다', code=400):
        super().__init__(msg=msg, code=code)


class CantModify(PostError):
    def __init__(self, msg='게시글의 수정/삭제가 불가능한 상태입니다', code=401):
        super().__init__(msg=msg, code=code)


class NotRecruiting(PostError):
    def __init__(self, msg='인원을 모집하지 않는 게시글입니다', code=402):
        super().__init__(msg=msg, code=code)


class MaxMember(PostError):
    def __init__(self, msg='현재 참여자 수가 최대 인원에 도달하여 참가할 수 없습니다', code=403):
        super().__init__(msg=msg, code=code)


class OwnerQuit(PostError):
    def __init__(self, msg='대표 유저는 게시글을 탈퇴할 수 없습니다', code=404):
        super().__init__(msg=msg, code=code)


class AlreadyJoinedUser(PostError):
    def __init__(self, msg='이미 참여가 완료된 유저입니다', code=405):
        super().__init__(msg=msg, code=code)


class NotJoinedUser(PostError):
    def __init__(self, msg='참여하지 않은 유저입니다', code=406):
        super().__init__(msg=msg, code=code)


class NotValidStatus(PostError):
    def __init__(self, msg='유효하지 않은 상태 메시지입니다', code=407):
        super().__init__(msg=msg, code=code)


class BeforeDelivered(PostError):
    def __init__(self, msg='배달 완료 이전에는 계좌번호를 확인할 수 없습니다', code=408):
        super().__init__(msg=msg, code=code)


class AccountQueryTimeout(PostError):
    def __init__(self, msg='조회 가능 기간이 지났습니다', code=409):
        super().__init__(msg=msg, code=code)


# Order
class OrderError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotValidOrder(OrderError):
    def __init__(self, msg='주문 정보가 유효하지 않습니다', code=500):
        super().__init__(msg=msg, code=code)


# Comment
class CommentError(DomainError):
    def __init__(self, msg, code):
        super().__init__(msg=msg, code=code)


class NotExistComment(CommentError):
    def __init__(self, msg='댓글 정보를 찾을 수 없습니다', code=600):
        super().__init__(msg=msg, code=code)
