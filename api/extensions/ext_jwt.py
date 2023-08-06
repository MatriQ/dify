from datetime import timedelta
from flask_jwt_extended import JWTManager

from api.services.account_service import AccountService, TenantService


def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    account = AccountService.load_user(identity.id)
    account.current_tenant = TenantService.get_current_tenant_by_account(account)
    return account


def init_app(app):
    app.config['JWT_SECRET_KEY'] = app.secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)
    jwt = JWTManager(app)

    jwt.user_lookup_loader(user_lookup_callback)
