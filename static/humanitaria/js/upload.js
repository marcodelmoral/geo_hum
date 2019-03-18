$(function () {
    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#insert").hide()
    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: false,

        start: function (e) {
            $("#modal-progress").modal("show");
        },

        stop: function (e) {
            $("#modal-progress").modal("hide");
        },

        progressall: function (e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            $(".progress-bar").css({"width": strProgress});
            $(".progress-bar").text(strProgress);
        },

        done: function (e, data) {
            if (data.result.is_valid) {
                $("#insert").show();
                $("#insert").addClass("alert-primary");
                document.getElementById("insert").innerHTML = "Subido exitosamente";
            }
            else {
                $("#insert").show();
                $("#insert").addClass("alert-danger");
                document.getElementById("insert").innerHTML = data.result.errors;
            }
        }

    });

});