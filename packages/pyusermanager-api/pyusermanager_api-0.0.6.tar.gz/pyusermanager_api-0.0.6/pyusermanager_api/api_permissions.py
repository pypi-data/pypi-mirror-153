from sws_webstuff import *

from sanic import Sanic
from sanic.response import json
from http import HTTPStatus

from pyusermanager import Perm


async def get_perms(request):
    app = request.app

    success, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if not success:
        return json(
            get_json_from_args(
                Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.WARNING),
                Redirect("/login"),
                HTTPStatus.UNAUTHORIZED,
            )
        )

    # return users perms
    if not app.ctx.AuthProvider.is_in_group_by_name(found_username, app.ctx.cfg.admin_group_name):
        return json(
            get_json_from_args(Alert(app.ctx.lang.perm_admin_error, ALERT_TYPE.WARNING), Redirect("/")),
            HTTPStatus.UNAUTHORIZED,
        )

    return json(Perm(app.ctx.cfg, "test").get_all())


async def change_perm(request, add):
    app = request.app
    success, found_username = app.ctx.AuthProvider.is_logged_in(request.ctx.token, request.ctx.ip)

    if not success:
        return json(
            get_json_from_args(
                Alert(app.ctx.lang.not_logged_in, ALERT_TYPE.WARNING),
                Redirect("/login"),
            )
        )

    if not app.ctx.AuthProvider.is_in_group_by_name(found_username, app.ctx.cfg.admin_group_name):
        return json(get_json_from_args(Alert(app.ctx.lang.perm_admin_error, ALERT_TYPE.WARNING), Redirect("/")))

    try:
        perm_name = request.json["perm"]
        if len(perm_name) < 1 or perm_name == app.ctx.cfg.admin_group_name:
            raise Exception()
    except Exception:
        return json(get_json_from_args(Alert(app.ctx.lang.parameter_error, ALERT_TYPE.DANGER)))

    if add:
        if Perm(app.ctx.cfg, perm_name).create():
            return json(get_json_from_args(Alert(app.ctx.lang.perm_create)))
    else:
        if Perm(app.ctx.cfg, perm_name).delete():
            return json(get_json_from_args(app.ctx.lang.perm_delete))

    return json(get_json_from_args(Alert(app.ctx.lang.misc_error, ALERT_TYPE.WARNING)))
