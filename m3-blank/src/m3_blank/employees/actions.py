# coding: utf-8

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# Stdlib
import datetime

# 3rdparty
from django.db import models

# Recordpack
from m3.actions import Action
from recordpack import recordpack
from recordpack.provider import DjangoProxyProvider
from recordpack.be import BE
from recordpack.typecast import cast_to_date

# Employees
import ui
from proxy import EmployeeListProxy, EmployeeCardProxy
from models import Employee

from demo.models import Person

#------------------------------------------------------------------------------
# Demonstrative action packs
#------------------------------------------------------------------------------

class EmployeesPack(recordpack.BaseRecordListPack):
    u"""
    Recordpack для модели Employee.
    """

    url = '/employees'
    title = u'Сотрудники'
    title_plural = u'Сотрудники'

    edit_window = new_window = ui.EmployeeEditWindow
    list_window = ui.EmployeeListWindow

    provider = DjangoProxyProvider(
        data_source=Employee,
        list_proxy=EmployeeListProxy,
        card_proxy=EmployeeCardProxy)

    quick_filters = {
        'employee_full_name': {'control': {'xtype': 'textfield'}},
        'position_name': {'control': {'xtype': 'textfield'}},
    }

    sorting = ('employee__fname', 'position__pname')


