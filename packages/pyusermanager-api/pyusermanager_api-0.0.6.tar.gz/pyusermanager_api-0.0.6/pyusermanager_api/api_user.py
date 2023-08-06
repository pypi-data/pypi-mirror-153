from http import HTTPStatus, client
from sanic import Sanic
from sanic.response import json

from pyusermanager import *
from pyusermanager.Config import *
from pyusermanager.Config.db_providers import *

from sws_webstuff import *

from binascii import a2b_base64
import imghdr

from pyusermanager_api import api_misc


async def get_users(request):
    app = request.app

    success, username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)
    print(username)
    if success:
        return json({"Users": user(app.ctx.cfg).get_users()})
    else:
        return json(
            get_json_from_args(Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.DANGER), Redirect("/login")),
            HTTPStatus.UNAUTHORIZED,
        )


async def get_user_info(request, username):
    app = request.app

    success, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if not success:
        return json(
            get_json_from_args(Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.DANGER), Redirect("/login")),
            HTTPStatus.UNAUTHORIZED,
        )

    include_email = False

    user_obj = user(app.ctx.cfg, username)
    try:
        if app.ctx.AuthProvider.is_in_group(request.ctx.token, request.ctx.ip, app.ctx.cfg.admin_group_name):
            return json(get_json_from_args(user_obj.info_extended()))

        if found_username == username:
            include_email = True

        return json(user_obj.info(include_email))

    except PyUserExceptions.MissingUserException:
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_missing, ALERT_TYPE.DANGER), Redirect("/users")),
            HTTPStatus.BAD_REQUEST,
        )


async def get_info_for_header(request):
    app = request.app

    logged_in, username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)
    if logged_in:

        found_user = user(app.ctx.cfg, username)
        # check if user is admin!
        if app.ctx.AuthProvider.is_in_group_by_name(username, app.ctx.cfg.admin_group_name):
            return json(
                get_json_from_args(
                    {"admin": True},
                    found_user.info(False),
                    {"registration": app.ctx.cfg.public_registration},
                )
            )

        return json(
            get_json_from_args(
                found_user.info(False),
                {"registration": app.ctx.cfg.public_registration},
            )
        )

    return json({"registration": app.ctx.cfg.public_registration}, HTTPStatus.UNAUTHORIZED)


async def update_user_info(request, username):
    app = request.app

    logged_in, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if not logged_in:
        return json(get_json_from_args(Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.DANGER), Redirect("/login")))

    try:
        this_user = user(app.ctx.cfg, username)
        this_user.info()
    except Exception:
        return json(get_json_from_args(Alert(app.ctx.lang.user_missing, ALERT_TYPE.DANGER)))

    if not (
        found_username == this_user.username
        or app.ctx.AuthProvider.is_in_group_by_name(found_username, app.ctx.cfg.admin_group_name)
    ):
        return json(get_json_from_args(Alert(app.ctx.lang.perm_misc_error, ALERT_TYPE.DANGER)), HTTPStatus.UNAUTHORIZED)

    json_dict = request.json

    # print(json_dict["img"])
    img_base64 = json_dict.get("img", None)
    password = json_dict.get("password", None)
    passwordconfirm = json_dict.get("passwordconfirm", None)
    email = json_dict.get("email", None)

    if password != passwordconfirm:
        return json(
            get_json_from_args(Alert(app.ctx.lang.parameter_password_confirm_error, ALERT_TYPE.DANGER)),
            HTTPStatus.BAD_REQUEST,
        )

    try:
        if password is not None:
            this_user.change(password=password)

        if email is not None:
            this_user.change(email=email)

    except:
        return json(
            get_json_from_args(Alert(app.ctx.lang.parameter_generic_error, ALERT_TYPE.DANGER)), HTTPStatus.BAD_REQUEST
        )

    if img_base64 is not None:
        img_bytes = a2b_base64(img_base64)

        filetype = imghdr.what(None, h=img_bytes)
        if not (filetype == "gif" or filetype == "jpeg" or filetype == "png"):
            return json(
                get_json_from_args(Alert(app.ctx.lang.file_invalid_type, ALERT_TYPE.DANGER)), HTTPStatus.BAD_REQUEST
            )

        try:
            # create avatar file
            with open(f"{app.ctx.cfg.avatar_folder}/{username}", "wb") as avatarfile:
                avatarfile.write(img_bytes)

            this_user.change(avatar=username)
        except Exception:
            return json(
                get_json_from_args(Alert(app.ctx.lang.avatar_set_error, ALERT_TYPE.DANGER)),
                HTTPStatus.INTERNAL_SERVER_ERROR,
            )

    # change perm stuff if user is admin

    if app.ctx.AuthProvider.is_in_group_by_name(found_username, app.ctx.cfg.admin_group_name):
        perms = json_dict.get("perms", None)

        for perm, add in perms.items():
            print(perm, add)
            Perm(app.ctx.cfg, perm).perm_user(username, add)

    return json(get_json_from_args(Alert(app.ctx.lang.changes_success), Redirect(f"/user/{username}")))


async def delete_user(request, username):
    app = request.app

    logged_in, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    returnvalue = json(get_json_from_args(Alert(app.ctx.lang.user_delete_error, ALERT_TYPE.WARNING)))

    if not logged_in:
        return json(
            get_json_from_args(
                Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.WARNING), Redirect("/"), HTTPStatus.UNAUTHORIZED
            )
        )

    # allow user to delete himself
    if logged_in and found_username == username:
        user(app.ctx.cfg, username).delete()
        returnvalue = json(
            get_json_from_args(
                {"Logout": True},
                Alert(app.ctx.lang.user_delete_success, ALERT_TYPE.SUCCESS),
                Redirect("/"),
            )
        )
    # allow admins to delete users
    elif app.ctx.AuthProvider.is_in_group(request.ctx.token, request.ctx.ip, app.ctx.cfg.admin_group_name):
        user(app.ctx.cfg, username).delete()
        returnvalue = json(
            get_json_from_args(
                Alert(app.ctx.lang.user_delete_success, ALERT_TYPE.SUCCESS),
                Redirect("/users"),
            )
        )

    return returnvalue


async def create_by_admin(request):
    app = request.app

    logged_in, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if not app.ctx.AuthProvider.is_in_group_by_name(found_username, app.ctx.cfg.admin_group_name):
        return json(
            get_json_from_args(Alert(app.ctx.lang.perm_admin_error, ALERT_TYPE.DANGER), Redirect("/")),
            status=HTTPStatus.BAD_REQUEST,
        )
    try:
        json_dict = request.json
        password = json_dict["password"]
        username = json_dict["username"]
        email = json_dict["email"]
        perms = json_dict["perms"]

        await api_misc.create_user(app, password, username, email)

        for perm, add in perms.items():
            print(perm, add)
            Perm(app.ctx.cfg, perm).perm_user(username, add)

        return json(
            get_json_from_args(Alert(app.ctx.lang.user_create_success, ALERT_TYPE.SUCCESS)), status=HTTPStatus.OK
        )

    except Exception as err:
        print(err)
        return json(
            get_json_from_args(Alert(app.ctx.lang.user_create_error, ALERT_TYPE.DANGER)),
            status=HTTPStatus.BAD_REQUEST,
        )
