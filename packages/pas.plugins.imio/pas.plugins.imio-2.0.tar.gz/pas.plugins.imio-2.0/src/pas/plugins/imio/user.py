# -*- coding: utf-8 -*-
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import checkEmailAddress
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema
from zope.interface import implementer


@implementer(IUserDataSchemaProvider)
class UserDataSchemaProvider(object):
    def getSchema(self):
        """ """
        return IPASUserDataSchema


class IPASUserDataSchema(IUserDataSchema):
    """Use all the fields from the default user data schema, and add various
    extra fields.
    """

    # username = schema.TextLine(
    #     title=_(u"label_user_name", default=u"User Name"),
    #     description=_(
    #         u"help_user_name_creation", default=u"Enter user name, e.g. jsmith."
    #     ),
    #     required=False,
    #     readonly=True,
    # )

    fullname = schema.TextLine(
        title=_(u"label_full_name", default=u"Full Name"),
        description=_(
            u"help_full_name_creation", default=u"Enter full name, e.g. John Smith."
        ),
        required=False,
        readonly=True,
    )

    email = schema.ASCIILine(
        title=_(u"label_email", default=u"E-mail"),
        description=u"",
        required=True,
        readonly=True,
        constraint=checkEmailAddress,
    )


class PASUserDataPanelAdapter(UserDataPanelAdapter):
    """ """
