# coding: utf-8

from  TemplateListRenderMixin import TemplateListRenderMixin
from m3_ext.ui.controls.buttons import ExtButton



class SelectListMixin(object):
    """
    Класс примесь, наделяющая форму справочника возможностями выбора.
    Может использоваться если форма конечного справочника сильно отличается от базовой,
    чтобы не пришлось копипастить код в форму выбора.
    При наследовании важно не забыть прописать вызов конструктора примеси!
    """

    disable_date_filter_on_select = True
    disable_state_filter_on_select = True
    disable_ent_filter_on_select = True

    # При выборе из справочника возвращать в поле всю запись,
    # а не только id и name
    select_record = False

    # Имя колонки, данные из которой будут использованы в качестве
    # отображаемого значения для поля ExtDictSelectField.
    on_select_column_display = 'name'
    # Имя колонки, данные из которой будут использованы в качестве
    # идентификатора записи для поля ExtDictSelectField.
    on_select_column_id = 'id'

    def __init__(self):
        assert isinstance(self, TemplateListRenderMixin)
        self.templates_list.append('BaseSelectListWindow.js')

        # Модификация формы
        self.modal = True
        self.maximized = False
        self.grid.read_only = True

        # Добавляем кнопку выбора
        self.select_button = ExtButton(name='select_btn', text=(u'Выбрать'))
        self.buttons.insert(0, self.select_button)

        self.column_name_on_select = self.on_select_column_display
        self.id_name_on_select = self.on_select_column_id


        # Если форма поддерживает выбор периода и статуса, то их нужно отключить
        if hasattr(self, 'records_date_field'):
            self.records_date_field.read_only = self.disable_date_filter_on_select
        if hasattr(self, 'records_state_field'):
            self.records_state_field.read_only = self.disable_state_filter_on_select
        if hasattr(self, 'records_ent_field'):
            self.records_ent_field.read_only = self.disable_ent_filter_on_select

        self.set_multiselect_mode(False)

    def set_multiselect_mode(self, multiselect):
        """
        Изменяет обработчики на форме в зависимости от использования множественного выбора
        """
        top_bar = None
        if hasattr(self.grid, '_top_bar'):
            top_bar = self.grid._top_bar
        elif hasattr(self.grid, 'top_bar'):
            top_bar = self.grid.top_bar
        if multiselect:
            self.templates_list.append('InitMultiSelect.js')
            self.grid._listeners['rowdblclick'] = None
            self.select_button.handler = 'multiSelectValues'
            # Событие 65558. Отключим топбар
            if top_bar:
                top_bar.make_read_only(True, exclude_list=self._get_tool_bar_exclude_list())
        else:
            if self.select_record:
                handler = 'selectRecord'
            else:
                handler = 'selectValue'     # handler = 'selectValue'
            self.grid._listeners['rowdblclick'] = handler
            self.select_button.handler = handler
            # Событие 65558. Включим топбар
            if top_bar:
                top_bar.make_read_only(False, exclude_list=self._get_tool_bar_exclude_list())

    def _get_tool_bar_exclude_list(self):
        u"""Список кнопок для исключения в тулбаре
        """
        return []
