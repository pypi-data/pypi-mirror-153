from sanic import Sanic
from sanic.response import json
from http import HTTPStatus


from sws_webstuff import *
from . import api_misc

from pyusermanager import *

import re


async def register_user(request):

    app = request.app

    if not app.ctx.cfg.public_registration:
        return json(
            get_json_from_args(
                Alert(app.ctx.lang.registration_forbidden, ALERT_TYPE.WARNING),
                Redirect("/"),
            ),
            status=HTTPStatus.FORBIDDEN,
        )

    logged_in, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if logged_in:
        return json(
            get_json_from_args(Alert(app.ctx.lang.already_logged_in, ALERT_TYPE.WARNING), Redirect("/")),
            status=HTTPStatus.FORBIDDEN,
        )

    json_dict = request.json

    try:
        password = json_dict["password"]
        password_confirm = json_dict["passwordconfirm"]
        username = json_dict["username"]
        email = json_dict["email"]

        matched_username = re.search(r"[a-z,A-Z,_,0-9]*", username)
        print(matched_username)
        if username != matched_username.group():
            return json(
                get_json_from_args(Alert(app.ctx.lang.parameter_username_error, ALERT_TYPE.WARNING)),
                status=HTTPStatus.BAD_REQUEST,
            )

    except Exception as err:
        print(err)
        return json(
            get_json_from_args(Alert(app.ctx.lang.parameter_error, ALERT_TYPE.WARNING)),
            status=HTTPStatus.BAD_REQUEST,
        )

    if password != password_confirm:
        return json(
            get_json_from_args(Alert(app.ctx.lang.parameter_password_confirm_error, ALERT_TYPE.WARNING)),
            status=HTTPStatus.BAD_REQUEST,
        )
    try:
        await api_misc.create_user(app, password, email=email, username=username)
        return json(
            get_json_from_args(
                Alert(app.ctx.lang.user_create_success, ALERT_TYPE.SUCCESS),
                Redirect("/login"),
            ),
            status=HTTPStatus.CREATED,
        )
    except PyUserExceptions.AlreadyExistsException:
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_create_existing, ALERT_TYPE.DANGER)),
            status=HTTPStatus.BAD_REQUEST,
        )
    except (TypeError, ValueError) as err:
        print(err)
        return json(
            get_json_from_args(Alert(app.ctx.lang.parameter_error, ALERT_TYPE.DANGER)),
            status=HTTPStatus.BAD_REQUEST,
        )
