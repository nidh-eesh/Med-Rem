var appoint_date = null;
$(document).on('click', '.edit', function () {
    $(this).parent().siblings('td.data').each(function () {
        var content = $(this).html();
        $(this).html('<input type=datetime-local value="' + content + '">');
    });
    $(this).siblings('.save').show();
    /*$(this).siblings('.delete').hide();*/
    $(this).hide();

});
$(document).on('click', '.save', function () {
    $('input').each(function () {
        var content = $(this).val();
        $(this).html(content);
        $(this).contents().unwrap();
        appoint_date = content;
    });
    console.log(appoint_date)
    var id = $(this).parent().siblings('.patient_id').text();
    console.log(id);
    const userKeyRegExp = /^[0-9]{4}\-[0-1][0-9]\-[0-3][0-9]\T[0-2][0-9]\:[0-5][0-9]?$/;
    const valid = userKeyRegExp.test(appoint_date);
    if (valid) {
        confirm("Confirm Appointment Date Updation?")
        $.post('/records/', { appoint_date: appoint_date, patient_id: id, 'csrfmiddlewaretoken': '{{ csrf_token }}' }, function (result) {
            alert('Appointment updated successfully');
        });
    }
    else {
        alert("Please enter a valid date");
        location.reload()
    }
    $(this).siblings('.edit').show();
    /*$(this).siblings('.delete').show();*/
    $(this).hide();
});