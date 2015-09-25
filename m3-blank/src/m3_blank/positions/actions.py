# coding: utf-8

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

from m3.actions.packs import DictListWindowAction

# RecordPack
from recordpack import recordpack
from recordpack.provider import DjangoProxyProvider

# Positions
import ui
from proxy import PositionListProxy
from models import Position

#------------------------------------------------------------------------------
# Demonstrative action packs
#------------------------------------------------------------------------------

class PositionPack(recordpack.BaseRecordListPack):
    u"""
    RecordPack для модели Position.
    """
    url = '/pos'
    title = u'Должности'
    title_plural = u'Должности'

    edit_window = new_window = ui.PositionEditWindow
    list_window = ui.PositionListWindow

    provider = DjangoProxyProvider(
        data_source=Position,
        list_proxy=PositionListProxy)

    quick_filters = {
        'pcode': {'control': {'xtype': 'textfield'}},
        'pname': {'control': {'xtype': 'textfield'}},
    }

    sorting = ('pcode', 'pname')

