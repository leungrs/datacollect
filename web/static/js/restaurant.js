var $rest_table;

function InitRestTable () {
    //记录页面bootstrap-table全局变量$rest_table，方便应用
    $rest_table = $('#rest_table').bootstrapTable({
        url: "query",                      //请求后台的URL（*）
        method: 'post',                      //请求方式（*）
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
        pageSize: 10,                     //每页的记录行数（*）
        pageList: [10, 20, 30],        //可供选择的每页的行数（*）
        search: false,                      //是否显示表格搜索
        strictSearch: false,
        showColumns: false,                  //是否显示所有的列（选择显示的列）
        showRefresh: false,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        //height: 500,                      //行高，如果没有设置height属性，表格自动根据记录条数决定表格高度
        uniqueId: "id",                     //每一行的唯一标识，一般为主键列
        showToggle: false,                   //是否显示详细视图和列表视图的切换按钮
        cardView: false,                    //是否显示详细视图
        detailView: false,                  //是否显示父子表
        queryParams : function (params) {
            return params;
        },
        columns: [{
            field: 'id',
            title: 'ID'
        }, {
            field: 'uniform_credit_code',
            title: '社会统一信用代码'
        }, {
            field: 'ent_name',
            title: '企业名称'
        }, {
            field: 'province',
            title: '省份'
        }, {
            field:'id',
            title: '操作',
            width: 120,
            align: 'center',
            valign: 'middle',
            formatter: actionFormatter
        }],
        onLoadSuccess: function () {
        },
        onLoadError: function (e) {
            alert("数据加载失败！");
        }
    });
}

function actionFormatter(value, row, index, field){
    var id = row.id;
    var result = "<a class='p-1 text-success'  title='编辑' href='"+id+ "/update'><span class='oi oi-pencil'></span></a>"
    result += "<a class='p-1 text-success'  title='导出word' href='"+id+ "/export'><span class='oi oi-data-transfer-download'></span></a>"
    result += "<a data-uid='" + id + "' href='javascript:;' data-toggle='modal' data-target='#confirm_modal' class='p-1 text-danger' title='删除'><span class='oi oi-delete'></span></a>";
    return result;
}

register_confirm_ok_handler(function(){
    uid = $("#confirm_dialog_value").val()
    $.ajax({
        url: uid+"/delete",
        type: "post",
        processData: false,
        contentType: false,
        success: function() {
            $rest_table.bootstrapTable("refresh");
        },
        error: function() {
            alert("删除失败!");
        }
    });
});


InitRestTable();