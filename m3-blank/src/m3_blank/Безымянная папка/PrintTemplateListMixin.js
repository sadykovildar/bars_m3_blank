
var columnsType = {};
{% for column, type in component.columns_type_for_print.items %}
    columnsType['{{ column }}'] = '{{ type }}';
{% endfor %}


function getCellId(grid) {
    //значит модель выделения ячейками:
    var recId = grid.getSelectionModel().getSelectedCell();
    return grid.getStore().getAt(recId[0]).id;
}

function printDocument(url, report_id, pack_shortname, multiselect, grid_id, not_need_selection) {
    var grid = Ext3.getCmp(grid_id);
    var recId;

    if (not_need_selection) {
        // выбор записей не требуется
    }
    // Если это tree grid, то
    else if (grid instanceof Ext3.m3.ObjectTree){
        if (!grid.getSelectionModel().getSelectedNode()) {
            Ext3.Msg.show({
                title:'Внимание!',
                msg: 'Не выбрана запись для печати',
                buttons: Ext3.Msg.OK,
                icon: Ext3.MessageBox.WARNING
            });
            return
        }
        if (multiselect) {
            Ext3.Msg.show({
                title:'Внимание!',
                msg: 'Множественная печать не поддерживается',
                buttons: Ext3.Msg.OK,
                icon: Ext3.MessageBox.WARNING
            });
            return
        } else {
            if (grid.getSelectionModel().getSelectedNode()) {
                recId = grid.getSelectionModel().getSelectedNode().id;
            }
        }
    }
    // Если это обычный грид
    else{
        if (!multiselect & !grid.getSelectionModel().hasSelection()) {
            Ext3.Msg.show({
                title:'Внимание!',
                msg: 'Не выбрана запись для печати',
                buttons: Ext3.Msg.OK,
                icon: Ext3.MessageBox.WARNING
            });
            return
        }
        if (multiselect) {
            //Надо сделать мнрожетсвенный выбор:
            recId = [];
            if (grid.getSelectionModel().hasSelection()) {
                // Если что-то выбрано:
                if (grid.getSelectionModel().getSelections) {
                    //значит модель выделения строками:
                    Ext3.each(grid.getSelectionModel().getSelections(), function(row){
                        recId.push(row.id);
                    });
                } else {
                    //значит модель выделения ячейками:
                    recId = getCellId(grid);
                }
            }// если ничего не выбрано то и отправим пустой список:
            recId = Ext3.util.JSON.encode(recId);
        } else {
            if (grid.getSelectionModel().getSelections) {
                recId = grid.getSelectionModel().getSelected().id;
            } else {
                recId = getCellId(grid);
            }
        }
    }

    var mask = new Ext3.LoadMask(win.body);
    var params = Ext3.applyIf({
            report_id: report_id, pack_shortname: pack_shortname
        }, win.actionContextJson
    );
    var tmp;
    //Блок сгенерирован шаблонизатором
    {%for cmp_id in component.PRINT_PARAMS %}
    tmp = Ext3.getCmp('{{cmp_id}}');
    params[tmp.name] = tmp.getValue();
    //Блок сгенерирован шаблонизатором
    {% endfor %}

    if (!not_need_selection) {
        params[grid.rowIdName] = recId;
    }

    // если в параметрах есть массивы, то они должны быть сериализованы
    for (var i in params){
        if (params[i] instanceof Array){
            params[i] = Ext3.util.JSON.encode(params[i]);
        }
    }
    mask.show();
    Ext3.Ajax.request({
        url: url,
        params: params,
        success: function(response, opts) {
            smart_eval(response.responseText);
            mask.hide();
        },
        failure: function () {
            mask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
    });
};


/**
 * Печать журнала
 * @param url
 */
function printJournal(url, gridClientId) {
    var gridId = gridClientId || '{{ component.grid.client_id }}';
    var cmpGrid = Ext3.getCmp(gridId);
    //exportData(cmpGrid, url);

    // расширим буфер гриду для получения всех строк - сами виноваты
    var totalCount = cmpGrid.store.getTotalCount();
    if (cmpGrid.store.bufferSize < totalCount) {
        cmpGrid.store.bufferSize = totalCount;
        cmpGrid.store.on('load', function(){
            exportData(cmpGrid, url);
        }, this, {single: true});
        cmpGrid.view.reset(true);
    } else {
        exportData(cmpGrid, url);
    }
}

/**
 * Печать грида
 * @param grid
 * @param url
 */
function exportData(grid, url) {
    var columns = [];
    Ext3.each(grid.colModel.config, function(column,index) {
        var dataindex;
        if (column.dataIndex=='candidate') dataindex = column.nameField
        else dataindex = column.dataIndex
        columns.push({
            data_index: dataindex,
            header: column.header,
            id: column.id,
            sortable: column.sortable,
            width: column.width,
            hidden: column.hidden,
            summary_type: column.summaryType,
            num_format: column.num_format
        });
    });
    var banded_columns = [];
    if (grid.colModel.rows) {

        Ext.each(grid.colModel.rows, function(row) {
            var rec = [];
            if (row === undefined) {
                return false;
            }

            Ext3.each(row, function (column) {
                rec.push({
                    colspan: column.colspan,
                    width: column.width || -1,
                    header: column.header || '',
                    hidden: column.hidden || false
                });
            });

            banded_columns.push(rec);
        });

    }
    var data = [];
    Ext3.each(grid.store.data.items, function(item, index) {
        var obj = {};
        Ext3.apply(obj, item.json);
        data.push(obj);
    });

    var footer_data = [];
    var field = {};
    Ext3.each(columns, function(column, index) {
        if (column.summary_type && grid.store.totalRow) {
            field[column.data_index] = grid.store.totalRow[column.data_index];
        }
        if (column.data_index=="grouping") {
            var store = grid.getStore().data;
            var item, grouped, fld_name_data;

            item = store.items[index].json;
            grouped = item.grouped;
            if (grouped!=[]) {
                for (var i=0; i<store.length; i++) {
                    Ext3.each(grouped, function(group, index_g) {
                        if (group.substring(group.length-3)=="_id") grouped[index_g] = group.substr(0,group.length-3);
                    });
                    var index_g = store.items[i].json.indent;
                    fld_name = grouped[index_g];
                    if (fld_name=="candidate") fld_name = "fullname";
                    fld_name_data = data[i][fld_name];
                    if (fld_name_data==undefined) fld_name_data="";

                    if (index_g==0) data[i]["grouping"] = fld_name_data;
                    else data[i]["grouping"] = "  ".repeat(index_g) + fld_name_data;
                }
            }
        }
    });

    footer_data.push(field);

    var params = {
        banded_columns: Ext3.encode(banded_columns),
        columns: Ext3.encode(columns),
        title: win.title || '',
        columns_type: Ext.encode(columnsType),
        data: Ext3.encode(data),
        footer_data: Ext3.encode(footer_data),
        total_manual_counting: '{{ component.total_manual_counting }}',
        landscape: true
    };

    win.fireEvent('beforePrintGrid', params);

    var mask = new Ext3.LoadMask(grid.body);
    mask.show();
    Ext3.Ajax.request({
        url : url,
        params : params,
        success : function(res){
            mask.hide();
            var iframe = document.getElementById("hiddenDownloader");
            if (iframe === null)
            {
                iframe = document.createElement('iframe');
                iframe.id = "hiddenDownloader";
                iframe.style.visibility = 'hidden';
                document.body.appendChild(iframe);
            }
            iframe.src = res.responseText;
        },
        failure : function(){
            mask.hide();
            uiAjaxFailMessage.apply(this, arguments);
        }
    });
}
