# coding: utf-8

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# 3rdparty
from django.conf import urls
from m3_ext.ui import app_ui
from m3.actions import ControllerCache

# Positions
import actions
from demo import controller

#------------------------------------------------------------------------------
# Action packs registration
#------------------------------------------------------------------------------



def register_actions():
    controller.action_controller.extend_packs([
        actions.PositionPack(),
    ])


def register_desktop_menu():
    metarole = app_ui.GENERIC_USER
    positions_shortcut = app_ui.DesktopShortcut(
        name=u'Должности',
        pack=ControllerCache.find_pack(actions.PositionPack),
        index=10)
    app_ui.DesktopLoader.add(
        metarole, app_ui.DesktopLoader.TOPTOOLBAR, positions_shortcut)
    app_ui.DesktopLoader.add(
        metarole, app_ui.DesktopLoader.START_MENU, positions_shortcut)