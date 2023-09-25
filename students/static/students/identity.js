function clearInput() {
    $('#photo-clear_id').prop('checked', true)
    $('#photo_input').val('')
    $('#photo_profil').attr('src', 'https://via.placeholder.com/150')
}

$('#photo_input').change(function () {
    let [photo] = $('#photo_input').prop('files')
    if (photo) {
        $('#photo_profil').attr('src', URL.createObjectURL(photo))
    }
})

$(function () {
    $('#id_birthdate').datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: '-80:+5',
        dateFormat: 'dd/mm/yy',
    })
})
