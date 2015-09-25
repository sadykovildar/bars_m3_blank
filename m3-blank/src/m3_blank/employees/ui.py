# coding: utf-8
u"""
Пользовательский интерфейс (окошки).
"""
#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# 3rdparty
from django.db import models
from m3_ext.ui.windows.edit_window import ExtEditWindow
from m3_ext.ui.controls.buttons import ExtButton
from m3_ext.ui.containers.containers import ExtToolBar
from m3_ext.ui.windows.window import ExtWindow
from m3_ext.ui.panels.grids import ExtObjectGrid
from m3_ext.ui.containers.forms import ExtForm
from m3_ext.ui.fields import complex as fields
from m3_ext.ui.misc import store as stores

# Employee
import actions
from models import Employee

# Demo
from demo.models import Person
from demo.actions import PersonPack

# Positions

from positions.models import Position
from positions.actions import PositionPack

#------------------------------------------------------------------------------
# Windows
#------------------------------------------------------------------------------

class EmployeeEditWindow(ExtEditWindow):
    def __init__(self, create_new=True, *args, **kwargs):
        super(EmployeeEditWindow, self).__init__(*args, **kwargs)
        self.icon_cls = 'icon-application-edit'
        self.min_width, self.min_height = self.width, self.height = 400, 230
        self.modal = True
        self.form = ExtForm()

        self.button_align = self.align_left
        self.save_button = ExtButton(
            text=u'Сохранить',
            handler='submitForm')
        self.cancel_button = ExtButton(
            text=u'Закрыть',
            handler='function(){win.close();}')

        self.footer_bar = ExtToolBar()
        self.footer_bar.items.extend([
            self.save_button,
            self.cancel_button,
        ])

        self.init_component(*args, **kwargs)
        self.init_main_form()

    def init_main_form(self):

        # ФИО сотрудника
        # -------------------------------------------------------------
        ename_field = fields.ExtDictSelectField()
        ename_field.label = u'ФИО сотрудника'
        ename_field.name = 'employee_id'
        ename_field.max_length = 255
        ename_field.anchor = '100%'
        ename_field.allow_blank = False
        ename_field.display_field = 'fullname'
        ename_field.hide_clear_trigger = True
        ename_field.hide_dict_select_trigger = False
        ename_field.hide_edit_trigger = True
        ename_field.pack = PersonPack

        self.ename_field = ename_field
        self.form.items.append(ename_field)


        # Должность
        # -------------------------------------------------------------
        pos_name_field = fields.ExtDictSelectField()
        pos_name_field.label = u'Должность'
        pos_name_field.name = 'position_id'
        pos_name_field.max_length = 255
        pos_name_field.anchor = '100%'
        pos_name_field.allow_blank = False
        pos_name_field.display_field = 'pname'
        pos_name_field.hide_clear_trigger = True
        pos_name_field.hide_dict_select_trigger = True
        pos_name_field.hide_trigger = False
        pos_name_field.hide_edit_trigger = True
        pos_name_field.pack = PositionPack

        self.pos_name_field = pos_name_field
        self.form.items.append(pos_name_field)


class EmployeeListWindow(ExtWindow):
    columns = {
        'header': u'ФИО сотрудника',
        'data_index': 'employee_full_name',
        'sortable': True,
    }, {
        'header': u'Должность',
        'data_index': 'position_name',
        'sortable': True,
    }

    def __init__(self, *args, **kwargs):
        ExtWindow.__init__(self, *args, **kwargs)
        self.icon_cls = 'icon-application-view-list'
        self.modal = False
        self.layout = 'border'
        self.width, self.height = 800, 600
        self.maximized = True
        self.maximizable = True
        self.minimizable = True
        self.grid = self._create_grid()
        self.items.append(self.grid)
        self.init_component(*args, **kwargs)

    def _create_grid(self):
        grid = ExtObjectGrid(region='center')
        grid.groupable = False
        for column in self.columns:
            grid.add_column(**column)
        return grid

    def _add_clear_filters(self):
        self.cancel_button = ExtButton(
            text=u'Закрыть',
            handler='function(){win.close();}')
