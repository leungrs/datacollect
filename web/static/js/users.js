var $user_table;

function InitUserTable () {
    //记录页面bootstrap-table全局变量$user_table，方便应用
    $user_table = $('#user_table').bootstrapTable({
        url: "query_user",                      //请求后台的URL（*）
        method: 'post',                      //请求方式（*）
        //toolbar: '#toolbar',              //工具按钮用哪个容器
        striped: true,                      //是否显示行间隔色
        cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
        pageNumber: 1,                      //初始化加载第一页，默认第一页,并记录
        pageSize: 10,                     //每页的记录行数（*）
        pageList: [10, 20],        //可供选择的每页的行数（*）
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
            field: 'username',
            title: '用户名'
        }, {
            field: 'role',
            title: '角色'
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
    var role = row.role;
    var username = row.username;
    var result = "<a href='javascript:;' class='p-1 text-success'" +
    " data-userid='" + id + "' data-userrole='" + role + "' " + "' data-username='" + username + "' " +
    "data-toggle='modal' data-target='#user_modal' title='编辑'><span class='oi oi-pencil'></span></a>";
    result += "<a href='javascript:;' class='p-1 text-success' title='重置密码'><span class='oi oi-lock-locked'></span></a>";
    result += "<a href='javascript:;' class='p-1 text-danger' title='删除'><span class='oi oi-delete'></span></a>";
    return result;
}

function editUser() {
    $("#user_id").val("");
    $("#username").val("")
    $("#role").val("user")
    $("#user_modal").modal("show");
}

function saveUser() {
    // 保存用户
    user_id = $("#user_id").val();
    username = $("#username").val()
    role = $("#role").val()
    $.ajax({
       "url": "save_user",
       "type": "post",
       "data": JSON.stringify({
          "user_id": user_id,
          "username": username,
          "role": role
       }),
       "contentType": "application/json",
       "success": function(data, a, b, c) {
            if (data.status == "ok") {
                $user_table.bootstrapTable("refresh");
                $("#user_modal").modal("hide");
            } else {
                alert(data.message || "保存失败。")
            }

       },
       "error": function() {
          alert("保存失败。")
       }
    });


}

$('#user_modal').on('show.bs.modal', function (event) {
    if (!event.relatedTarget) {
        return;
    }
    var relatedTarget = $(event.relatedTarget);
    var userid = relatedTarget.data('userid');
    var role = relatedTarget.data('userrole');
    var username = relatedTarget.data('username');

    var modal = $(this)
    modal.find("#user_id").val(userid);
    modal.find('#username').val(username)
    modal.find('#role').val(role)
});