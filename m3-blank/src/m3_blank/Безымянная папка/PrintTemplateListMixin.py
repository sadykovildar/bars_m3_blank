class PrintTemplateListMixin(object):
    u"""
        Миксин для наделения окна
        волшебной способностью генерировать кнопки
        для печатных форм.
    """
    def __init__(self):
        assert isinstance(self, BaseExtWindow)
        self.PRINT_PARAMS = []
        assert isinstance(self, TemplateListRenderMixin)
        self.templates_list.append('PrintTemplateListMixin.js')

    def add_print_button(self, pack_shortname, grid=None, addmenu=None):
        u"""
            Создает кнопку для печатной формы.
            addmenu - указывает на создание меню(в любом случае, даже если в
            фикстурах будет всего один отчет)
        """
        if grid is None:
            grid = getattr(self, 'grid', None)
            if not grid: # мы сделали все, что могли
                raise AttributeError('Error! Grid must be defined, not None!')

        handler = u"""
            function() {
                printDocument('%(url)s', '%(report_id)s', '%(pack_shortname)s', %(multiselect)s, '%(grid_id)s', %(not_need_selection)s)
            }"""
        self.print_element = get_report_laucher(
            pack_shortname, handler, ROUTER_SHORTNAME, grid.client_id, addmenu)
        grid.print_element = self.print_element
        if isinstance(grid, ExtMultiGroupinGrid):
            grid._top_bar.items.append(self.print_element)
        else:
            grid.top_bar.items.append(self.print_element)

    def add_print_params(self, fields):
        u"""
            Регистрируем поля,
            из которых будем брать значения
            при отправке запроса на печать.
        """
        for fld in fields:
            self.PRINT_PARAMS.append(fld.client_id)