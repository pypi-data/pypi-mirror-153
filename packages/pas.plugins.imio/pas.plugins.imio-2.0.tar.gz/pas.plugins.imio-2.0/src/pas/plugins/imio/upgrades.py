from BTrees.OOBTree import OOBTree
from plone import api
from pas.plugins.imio.browser.view import AddAuthenticUsers
from authomatic.core import User

import logging

logger = logging.getLogger(__file__)


def set_new_userid(context=None):
    portal = api.portal.get()
    view = AddAuthenticUsers(portal, portal.REQUEST)
    users = view.get_authentic_users()

    acl_users = api.portal.get_tool("acl_users")
    plugin = acl_users.authentic
    plugin._useridentities_by_login = OOBTree()
    provider_name = "authentic-agents"

    for data in users:
        data["id"] = data["uuid"]
        user = User(provider_name, **data)
        userlogin = user.username
        userid = user.id
        saved_user = plugin._useridentities_by_userid.get(userlogin)
        saved_user.userid = userid
        saved_user.login = userlogin
        # __import__("ipdb").set_trace()
        # saved_user._identities["authentic-agents"].update({"user_id": userid, "login": "userlogin"})
        plugin._useridentities_by_userid[userid] = saved_user
        plugin._useridentities_by_login[userlogin] = saved_user
        plugin._userid_by_identityinfo[(provider_name, userid)] = userid
        del plugin._useridentities_by_userid[userlogin]
        del plugin._userid_by_identityinfo[(provider_name, userlogin)]
        logger.info(
            "user updated, new id is:{}, new login is: {}".format(userid, userlogin)
        )
