// Принять дефект
$(document).on("click", ".accept-defect", function(e) {
    if(confirm("Вы уверенны что хотите принять этот дефект ?") == true)  {
        $('.table-defects').html('');
        var id = $(this).attr('id');
        $.ajax({
            url:  "/accept_a_defect", //url
            type: "POST", //метод отправки
            data: "defect_id=" + id, // Сеарилизуем объект
            success: function(response) { //Данные отправлены успешно
                $('.table-defects').html(response);
            }
        });
    }
});

// Отпись дефекта
$(document).on("click", "#defect_writing", function(e) {
    var id = $("#defect_id").val();
    var eliminated_description = $("#eliminated_description").val();

    $.ajax({
        url:  "/defect_writing", //url
        type: "POST", //метод отправки
        data: { defect_id: id, eliminated_description:eliminated_description },
        success: function(response) { //Данные отправлены успешно
        }
    });

});


// Виды дефектов (непринятые, принятые и т.д.)
$(document).on("click", ".defect_type", function(e) {
    $('.table-defects').html('');
    var defect_type = $(this).attr('id');
    $.ajax({
        url:  "defect_type", //url
        type: "POST", //метод отправки
        data: "defect_type=" + defect_type, // Сеарилизуем объект
        success: function(response) { //Данные отправлены успешно
            $('.table-defects').html(response);
        }
    });
});
