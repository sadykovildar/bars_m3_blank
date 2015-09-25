class TemplateListRenderMixin(object):
    """
    Изменяет метод рендеринга шаблонов формы с "матрешечного" на списочный.

    "Матрешечный" способ подразумевает использование джанговского
    наследования шаблонов, т.е. директив extends и block внутри шаблона.
    Это ограничивает наследование, т.к. в наследнике нужно знать имя
    шаблона предка. Практика показывает, что такой способ гибок, но редко
    нужен, часто достаточно просто прибавлять новый шаблон
    в начало старого.

    Списочный способ позволяет не заботится о имени предка, только вместо
    template_globals нужно использовать templates_list.
    При наследовании от старых форм, template_globals будет добавляться
    в начало templates_list.

    """

    # Список имён файлов дополнительных js-шаблонов,
    # которые должно использовать окно.
    js_templates = []

    def __init__(self, *args, **kwargs):
        self.templates_list = []
        super(TemplateListRenderMixin, self).__init__(*args, **kwargs)

        self.templates_list.extend(self.js_templates)

    def render_globals(self):
        result = ''
        if self.template_globals:
            self.templates_list.insert(0, self.template_globals)

        default_dict = {'component': self, 'window': self}
        context = Context(default_dict)
        for file_name in self.templates_list:
            if isinstance(file_name, (tuple, list)):
                file_context = Context(default_dict)
                file_context.update(file_name[1])
                file_name = file_name[0]
            else:
                file_context = context
            template = get_template(file_name)
            try:
                text = template.render(file_context)
            except Exception as err:
                # не надо молчать если есть проблемы
                raise ApplicationLogicException(
                    'Render error for template {} {}'.format(
                        file_name,
                        get_exception_description(err)))

            # Комментарий для отладки
            remark = '\n//========== TEMPLATE: %s ==========\n' % file_name
            result += remark + text

        # Отмечает строку как безопасную (фильтр safe) для шаблонизатора
        return mark_safe(result)