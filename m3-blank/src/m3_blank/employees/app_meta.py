# coding: utf-8

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# 3rdparty
from django.conf import urls
from m3_ext.ui import app_ui
from m3.actions import ControllerCache

# Employees
import actions
from demo import controller

#------------------------------------------------------------------------------
# Action packs registration
#------------------------------------------------------------------------------



def register_actions():
    controller.action_controller.extend_packs([
        actions.EmployeesPack(),
    ])


def register_desktop_menu():
    metarole = app_ui.GENERIC_USER
    employeess_shortcut = app_ui.DesktopShortcut(
        name=u'Сотрудники',
        pack=ControllerCache.find_pack(actions.EmployeesPack),
        index=10)
    app_ui.DesktopLoader.add(
        metarole, app_ui.DesktopLoader.TOPTOOLBAR, employeess_shortcut)
    app_ui.DesktopLoader.add(
        metarole, app_ui.DesktopLoader.START_MENU, employeess_shortcut)