import logging
from logging.handlers import RotatingFileHandler
from flask import request, g

request_logger = logging.getLogger('request_logger')
request_logger.setLevel('INFO')

rotating_file_handler = RotatingFileHandler(filename='log/log.txt', maxBytes=10 * 512)
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(message)s")
rotating_file_handler.setFormatter(formatter)
request_logger.addHandler(rotating_file_handler)


def request_log(response):
    ip = request.remote_addr
    ip_list = request.environ.get('X-Forwarded-For')
    if ip_list:
        ip = ip_list[0]

    msg = {
        'ip': ip,
        'method': request.method,
        'path': request.path,
        'status_code': response.status_code
    }

    try:
        msg['id'] = g.id
        msg['nickname'] = g.nickname
    except AttributeError:
        pass

    if request.content_type == 'application/json':
        data = request.get_json()
        if '/auth/login' != request.path:
            msg['request'] = data

    msg['response'] = response.get_json()
    request_logger.info(f'msg: {msg}')
