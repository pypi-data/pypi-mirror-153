import pyusermanager
from pyusermanager import *
from pyusermanager.Config import *
from pyusermanager.Config.db_providers import *
from sanic import Sanic


def configure(config_paras: dict, app):

    ##########################################
    #                                        #
    # General Config Setup for Pyusermanager #
    #                                        #
    ##########################################

    if config_paras["db"]["connection-settings"].get("port", None):
        config_paras["db"]["connection-settings"]["port"] = int(config_paras["db"]["connection-settings"]["port"])

    db_cfg = DBProviders[config_paras["db"]["provider"]].value(**config_paras["db"]["connection-settings"])

    if config_paras.get("LDAP", False):
        ad_cfg = AD_Config(login=True, **config_paras["LDAP"])
    else:
        ad_cfg = AD_Config()

    cfg = General_Config(
        auto_activate_accounts=config_paras["general"].as_bool("auto_activate_accounts"),
        email_required=config_paras["general"].as_bool("email_required"),
        admin_group_name=config_paras["general"]["admin_group_name"],
        public_registration=config_paras["general"].as_bool("public_registration"),
        allow_avatars=config_paras["general"].as_bool("allow_avatars"),
        password_reset_days_valid=int(config_paras["general"]["password_reset_days_valid"]),
        username_min_len=int(config_paras["general"]["username_min_len"]),
        password_min_len=int(config_paras["general"]["password_min_len"]),
        adcfg=ad_cfg,
        avatar_folder = config_paras["avatar_folder"]
    )
    cfg.bind(db_cfg)

    # adding cfg to context
    app.ctx.cfg = cfg

    app.ctx.AuthProvider = AuthProvider(cfg)
