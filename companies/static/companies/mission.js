$(function () {
    $('#id_beginning_date').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd/mm/yy',
    })

    $('#id_ending_date').datepicker({
        changeMonth: true,
        changeYear: true,
        dateFormat: 'dd/mm/yy',
    })
})

$(function () {
    $('#id_proposed_job').autocomplete({
        source: function (request, response) {
            var matcher = new RegExp(
                $.ui.autocomplete.escapeRegex(request.term),
                'i'
            )
            response(
                $.grep(professions, function (value) {
                    value = value.label || value.value || value
                    return matcher.test(value) || matcher.test(normalize(value))
                })
            )
        },
    })
    $('#id_job_location').autocomplete({
        source: cities,
    })
})

var accentMap = {
    é: 'e',
    è: 'e',
}
var normalize = function (term) {
    var ret = ''
    for (var i = 0; i < term.length; i++) {
        ret += accentMap[term.charAt(i)] || term.charAt(i)
    }
    return ret
}
