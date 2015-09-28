__author__ = 'ildar'

from m3_ext.ui.controls.buttons import ExtButton

class SelectButton(ExtButton):
    def __init__(self, *args, **kwargs):
        super(SelectButton, self).__init__(self, *args, **kwargs)
        self.template = 'ext-controls/my-select-buttons'