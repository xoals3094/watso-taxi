from config import kakao_pay


def to_hex_value(cost: int) -> str:
    value = hex((cost * 524288))[2:]
    return value


def create_url(kakao_pay_user_id: str, cost: int) -> str:
    return kakao_pay.kakao_pay_url + kakao_pay_user_id + to_hex_value(cost)
