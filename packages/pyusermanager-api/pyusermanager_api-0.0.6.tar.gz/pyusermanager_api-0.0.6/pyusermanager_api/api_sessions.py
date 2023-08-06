from sanic import json, Sanic
from .api_misc import *
from sws_webstuff import *
from http import HTTPStatus
from pyusermanager import *

async def login_user(request):

    app = request.app

    json_dict = request.json

    logged_in, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if logged_in:
        return json(
            get_json_from_args(
                Redirect("/user/" + found_username),
                Alert(app.ctx.lang.already_logged_in, ALERT_TYPE.INFO),
            ),
            status=HTTPStatus.FORBIDDEN,
        )

    username = json_dict.get("username", None)
    password = json_dict.get("password", None)
    remember_me = json_dict.get("remember_me", False)

    valid_days = 1

    if remember_me:
        valid_days = 365
    try:
        if not login(app.ctx.cfg, username, password):
            return json(
                get_json_from_args(Alert(app.ctx.lang.user_login_error, ALERT_TYPE.DANGER)),
                status=HTTPStatus.UNAUTHORIZED,
            )
    except PyUserExceptions.MissingUserException:
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_missing, ALERT_TYPE.DANGER)),
            status=HTTPStatus.UNAUTHORIZED,
        )
    except PyUserExceptions.ADLoginProhibited:
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_login_error, ALERT_TYPE.DANGER)),
            status=HTTPStatus.UNAUTHORIZED,
        )

    # create token
    authtoken = Token.Auth(app.ctx.cfg, username=username)
    authtoken.create(request.ctx.ip, valid_days)

    json_ret = get_json_from_args(
        Alert(app.ctx.lang.user_login_success),
        Redirect("/user/" + username),
        {"Login": {"token": authtoken.token}},
    )
    return json(json_ret, HTTPStatus.CREATED)

async def logout_user(request):

    app = request.app

    if not app.ctx.AuthProvider.is_logged_in(request.ctx.token,request.ctx.ip):
        return json(
            get_json_from_args(Alert(app.ctx.lang.not_logged_in), Redirect("/login")),
            status=HTTPStatus.FORBIDDEN,
        )

    authtoken = Token.Auth(app.ctx.cfg, request.ctx.token)
    try:
        authtoken.invalidate(request.ctx.ip)
        return json(get_json_from_args({"Logout": True}, Alert(app.ctx.lang.user_logout_success), Redirect("/")))
    except ValueError:
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_logout_error, ALERT_TYPE.WARNING)),
            status=HTTPStatus.BAD_REQUEST,
        )
