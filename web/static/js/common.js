function refresh_curr_page()
{
    window.location.reload();
}

function open_excel()
{
    $("#excel_import").click()
}

function import_excel(obj, excel_type)
{
    if ($(obj).val() == "") return;

    var file = document.getElementById("excel_import").files[0];
    var formData = new FormData();
    formData.append("file", file);
    formData.append("excel_type", excel_type);

    $.ajax({
        url: "/common/import",
        type: "post",
        processData: false,
        contentType: false,
        data: formData,
        success: function(result) {
            if (result.status == "fail") {
                alert("导入失败！");
            }
            else {
                alert("导入成功！");
                refresh_curr_page();
            }
            $(obj).val("");
        },
        error: function(xhr, status, err) {
            alert("导入失败");
        }
    });
}

function id_field_formatter(value, row, index, field)
{
    return "<a href='"+value+ "/update'>" + value + "</a>"
}

function op_formatter(value, row, index, field)
{
   rowid = row.id
   btn_del = "<button data-rowid=" +rowid+ " class='op_delete btn btn-primary'>删除</button>"
   btn_exp = "<a href='" +rowid+ "/export' class='ml-1 op_export btn btn-primary'>导出</a>"
   if (is_manager) {
      btn_exp += btn_del;
   }
   return btn_exp
}


$(document).on("click", ".op_delete", function(e) {
    rowid = this.dataset["rowid"];
    $.ajax({
        url: rowid+"/delete",
        type: "post",
        processData: false,
        contentType: false,
        success: function() {
            refresh_curr_page();
        },
        error: function() {
            alert("删除失败!");
        }
    });
});