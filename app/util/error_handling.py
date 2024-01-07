import exceptions


def format_error(api):
    @api.errorhandler(exceptions.FormatError)
    def format_error_handling(error):
        return error.json, 406


def auth_error_handler(api):
    login_error_handling(api)


def login_error_handling(api):
    @api.errorhandler(exceptions.NotExistToken)
    def not_exist_token_handling(error):
        return error.json, 401

    @api.errorhandler(exceptions.SigninFail)
    def signin_fail(error):
        return error.json, 401


def user_error_handling(api):
    @api.errorhandler(exceptions.NotExistUser)
    def not_exist_user(error):
        return error.json, 401

    signup_error_handling(api)
    profile_error_handling(api)
    device_error(api)


def device_error(api):
    @api.errorhandler(exceptions.DeviceNotFound)
    def device_not_found(error):
        return error.json, 404


def profile_error_handling(api):
    @api.errorhandler(exceptions.PasswordMismatch)
    def password_mismatch(error):
        return error.json, 401


def signup_error_handling(api):
    @api.errorhandler(exceptions.NotValidAuthCode)
    def not_valid_auth_code(error):
        return error.json, 401

    @api.errorhandler(exceptions.DuplicateUser)
    def duplicate_user_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotExistToken)
    def not_exist_token_handling(error):
        return error.json, 401

    @api.errorhandler(exceptions.ExpiredToken)
    def expired_token_handling(error):
        return error.json, 401


def delivery_error_handler(api):
    @api.errorhandler(exceptions.AccessDenied)
    def access_denied(error):
        return error.json, 403

    post_error_handler(api)
    store_error_handler(api)
    order_error_handler(api)
    comment_error_handler(api)


def post_error_handler(api):
    @api.errorhandler(exceptions.NotExistPost)
    def not_exist_post_handling(error):
        return error.json, 404

    @api.errorhandler(exceptions.CantModify)
    def cant_modify_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotRecruiting)
    def not_recruiting_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.AlreadyJoinedUser)
    def already_joined_user_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotJoinedUser)
    def not_joined_user_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.OwnerQuit)
    def owner_quit_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.MaxMember)
    def max_member_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotValidStatus)
    def not_valid_status_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.NotValidOrder)
    def not_valid_order_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.BeforeDelivered)
    def before_ordered_handling(error):
        return error.json, 406

    @api.errorhandler(exceptions.AccountQueryTimeout)
    def account_timeout_handling(error):
        return error.json, 406


def store_error_handler(api):
    @api.errorhandler(exceptions.NotExistStore)
    def not_exist_store_handling(error):
        return error.json, 404

    @api.errorhandler(exceptions.NotExistMenu)
    def not_exist_menu_handling(error):
        return error.json, 404


def order_error_handler(api):
    @api.errorhandler(exceptions.NotValidOrder)
    def not_valid_order_handling(error):
        return error.json, 406


def comment_error_handler(api):
    @api.errorhandler(exceptions.NotExistComment)
    def not_exist_comment_handling(error):
        return error.json, 404
