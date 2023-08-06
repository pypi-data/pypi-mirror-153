# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IContractsFolder(model.Schema):
    """Marker interface for ContractsFolder"""


@implementer(IContractsFolder)
class ContractsFolder(Container):
    pass
