var onSelectAttrDisplay = '{{ component.column_name_on_select }}',
    onSelectAttrId = '{{ component.id_name_on_select }}';


function isGridSelected(grid, title, message){
	var res = true;
	if (!grid.getSelectionModel().hasSelection() ) {
		Ext3.Msg.show({
		   title: title,
		   msg: message,
		   buttons: Ext3.Msg.OK,
		   icon: Ext3.MessageBox.INFO
		});
		res = false;
	}
	return res;
}

function selectValue(){
{% if component.action_context.select_record == 'true' %}

    /*
     * Позволяет определить в местах использования ExtDictSelectField
     * нужно ли получать запись целиком в результате выбора.
     * Для получения записи целиком нужно передать через action_context параметр select_record=True.
     */
    return selectRecord();

{% else %}

    var id,
        displayText,
        grid = Ext3.getCmp('{{ component.grid.client_id}}');

    if (!isGridSelected(grid, 'Выбор элемента', 'Выберите элемент из списка') ) {
        return;
    }

    id = grid.getSelectionModel().getSelected().get(onSelectAttrId);
    displayText = grid.getSelectionModel().getSelected().get(onSelectAttrDisplay);

    assert(id !== undefined, 'Справочник не определил id объекта. Поле выбора не будет работать');
    assert(displayText !== undefined, 'Справочник не определил displayText объекта. ' +
        'Возможно он не приходит с ajax ответом, в JsonStore нет соответствующего поля, ' +
        'в гриде нет соотв. колонки или неправильно указан column_name_on_select!');

    var win = Ext3.getCmp('{{ component.client_id}}');
    win.fireEvent('closed_ok', id, displayText);
    win.close();

{% endif %}
}

function selectRecord(){
    var record;
    var grid = Ext3.getCmp('{{ component.grid.client_id}}');
    if (!isGridSelected(grid, 'Выбор элемента', 'Выберите элемент из списка') ) {
        return;
    }
    record = grid.getSelectionModel().getSelected();
    var win = Ext3.getCmp('{{ component.client_id}}');
    win.fireEvent('closed_ok', record);
    win.close();
}

//методы для обеспечения множественного выбора
Ext3.apply(win, {

    initMultiSelect:function(selectedItems) {
        var grid = Ext3.getCmp('{{ component.grid.client_id}}');
        this.valueField = onSelectAttrId;
        this.checkedItems = this.extractSelectedData(selectedItems);
        this.grid = grid;
        grid.getStore().removeListener('load', this.onGridStoreLoad, this);
        grid.getStore().removeListener('rowselect', this.onCheckBoxSelect, this);
        grid.getStore().removeListener('rowdeselect', this.onCheckBoxDeselect, this);

        grid.getStore().on('load', this.onGridStoreLoad, this);

        grid.getSelectionModel().on('rowselect', this.onCheckBoxSelect, this);
        grid.getSelectionModel().on('rowdeselect', this.onCheckBoxDeselect, this);

        // #65558
        grid.topToolbar.hide();
    },
    
    extractSelectedData:function(selectedItems) {
        var i = 0, result = {};
        for(; i < selectedItems.length; i++) {
            result[selectedItems[i].data[this.valueField]] = selectedItems[i].copy();
        }
        return result;
    },

    checkSelectedItems:function(selectedItems) {
        this.grid = Ext3.getCmp('{{ component.grid.client_id}}');
        this.valueField = onSelectAttrId;
        this.checkedItems = this.extractSelectedData(selectedItems);
        this.grid.getStore().on('load', this.onGridStoreLoad, this);
    },

    onGridStoreLoad:function(store, records, options) {
        var selectAll = true;
        var i = 0, j = 0, recordsToSelect = [];
        for (;i< records.length;i++) {
            if (this.checkedItems[records[i].data[this.valueField]]) {
                recordsToSelect.push(records[i]);
            } else {
                selectAll = false
            }
        }
        if (selectAll){
            this.grid.getSelectionModel().selectAll(true);
        } else {
            this.grid.getSelectionModel().selectRecords(recordsToSelect);
        }
    }, 

    onCheckBoxSelect:function(selModel, rowIndex, record) {
        if (record){
            if (!this.checkedItems[record.data[this.valueField]] ) {
                this.checkedItems[record.data[this.valueField]] = record;
            }
        } else {
            return false;
        }
    },

    onCheckBoxDeselect:function(selModel, rowIndex, record) {
        if (record){
            if (this.checkedItems[record.data[this.valueField]]) {
                this.checkedItems[record.data[this.valueField]] = undefined;
            }
        } else {
            return false;
        }
    }
});


function multiSelectValues() {
    var records = [],
        win = Ext3.getCmp('{{ component.client_id}}'),
        grid = Ext3.getCmp('{{ component.grid.client_id}}');

    for (var checkedId in win.checkedItems) {
        if (win.checkedItems.hasOwnProperty(checkedId)) {

            var selected = win.checkedItems[checkedId];
            if (selected === undefined) {
                continue;
            }

            // Поддержка переопределенного поля, содержащего id записи.
            selected.set('custom_id_attr', onSelectAttrId);
            selected.set('custom_id_attr_val', selected.get(onSelectAttrId));

            if (selected.data.display === undefined) {
                // Поддержка переопределенного поля, содержащего значение
                // для отображения.
                var display = selected.get(onSelectAttrDisplay);
                if (display) {
                    selected.data.display = display;
                }
            }
            records.push(selected);
        }
    }
    if (!records.length){
        Ext3.Msg.show({
            title: 'Выбор элементов',
            msg: 'Выберите элементы из списка',
            buttons: Ext3.Msg.OK,
            icon: Ext3.MessageBox.INFO
        });
        return;
    }

	if (win.fireEvent('closed_ok', records) !== false &&
            win.fireEvent('multiSelected', records) !== false) {
        win.close();
    }
}

{% block extension %}
{% endblock %}
