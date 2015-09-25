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
from m3_ext.ui.fields import simple as fields
from m3_ext.ui.misc import store as stores

#------------------------------------------------------------------------------
# Windows
#------------------------------------------------------------------------------

class PositionEditWindow(ExtEditWindow):
    def __init__(self, create_new=True, *args, **kwargs):
        super(PositionEditWindow, self).__init__(*args, **kwargs)
        self.icon_cls = 'icon-application-edit'
        self.min_width, self.min_height = self.width, self.height = 400, 130
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

        # Код
        # -------------------------------------------------------------
        pcode_field = fields.ExtStringField()
        pcode_field.label = u'Код'
        pcode_field.name = 'pcode'
        pcode_field.max_length = 5
        pcode_field.regex = '^[0-9]{5}$'
        pcode_field.regex_text = u'Код должен состоять из 5 цифр'
        pcode_field.anchor = '100%'
        pcode_field.allow_blank = False

        self.pcode_field = pcode_field
        self.form.items.append(pcode_field)

        # Наименование
        # -------------------------------------------------------------
        pname_field = fields.ExtStringField()
        pname_field.label = u'Наименование'
        pname_field.name = 'pname'
        pname_field.max_length = 255
        pname_field.anchor = '100%'
        pname_field.allow_blank = False

        self.pname_field = pname_field
        self.form.items.append(pname_field)


class PositionListWindow(ExtWindow):

    columns = {
        'header': u'Код',
        'data_index': 'pcode',
        'sortable': True,
    }, {
        'header': u'Наименование',
        'data_index': 'pname',
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