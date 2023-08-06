import os
from sanic import Sanic
from sanic.response import json, file

import pyusermanager
from pyusermanager import *
from pyusermanager.Config import *
from pyusermanager.Config.db_providers import *
import pyusermanager.Token as Token


async def version(request):
    return json({"version": pyusermanager.__version__})


async def get_avatar(request, avatarname):
    app = request.app

    avatarlist = os.listdir(app.ctx.cfg.avatar_folder)

    if avatarname in avatarlist:
        return await file(f"{app.ctx.cfg.avatar_folder}/{avatarname}")
    else:
        return await file(f"{app.ctx.cfg.avatar_folder}/404.png")


async def create_user(app, password, username, email):
    user(app.ctx.cfg, username).create(password, email=email)
