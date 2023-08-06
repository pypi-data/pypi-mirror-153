# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IContract(model.Schema):
    """Marker interface for Contract"""


@implementer(IContract)
class Contract(Container):
    pass
