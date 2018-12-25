function open_excel() {
    $("#excel_import").click()
}

function import_excel(obj, excel_type) {
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

$('#confirm_modal').on('show.bs.modal', function (event) {
    if (!event.relatedTarget) {
        return;
    }
    var relatedTarget = $(event.relatedTarget);
    var uid = relatedTarget.data('uid');
    var modal = $(this)
    modal.find("#confirm_dialog_value").val(uid);
});

function register_confirm_ok_handler(handler) {
    $("#btn_confirm_ok").click(handler);
}