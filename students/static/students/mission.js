$(function () {
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
    $('#jobs').autocomplete({
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
        select: function (event, ui) {
            let val = $('#id_demanded_jobs').val()
            if (val == '') {
                $('#id_demanded_jobs').val(ui.item.value)
            } else {
                $('#id_demanded_jobs').val(val.concat(',', ui.item.value))
            }

            $('#demanded_jobs').append(`
            <li class="list-group-item d-flex align-items-center" id="${ui.item.value}">
                ${ui.item.value}
                <button type="button" job="${ui.item.value}" onclick="remove_job(this.getAttribute('job'))" class="btn-close ms-2" aria-label="Close"></button>
            </li>`)
            $(this).val('')
            return false
        },
    })
})

$(function () {
    $('#domains').autocomplete({
        source: domains,
        select: function (event, ui) {
            let val = $('#id_demanded_domains').val()
            if (val == '') {
                $('#id_demanded_domains').val(ui.item.value)
            } else {
                $('#id_demanded_domains').val(val.concat('|', ui.item.value))
            }

            $('#domains_chosen').append(`
            <li class="list-group-item d-flex align-items-center" id="${ui.item.value}">
                ${ui.item.value}
                <button type="button" domain="${ui.item.value}" onclick="remove_domain(this.getAttribute('domain'))" class="btn-close ms-2" aria-label="Close"></button>
            </li>`)
            $(this).val('')
            return false
        },
    })
})

function remove_job(job) {
    $(`[id="${job}"]`).remove()

    let arr = $('#id_demanded_jobs').val().split(',')
    arr = arr.filter((item) => item !== job)
    $('#id_demanded_jobs').val(arr[0])
    arr.forEach(function (item, index) {
        if (index !== 0) {
            let val = $('#id_demanded_jobs').val()
            $('#id_demanded_jobs').val(val.concat(',', item))
        }
    })
}

function remove_domain(domain) {
    $(`[id="${domain}"]`).remove()
    let arr = $('#id_demanded_domains').val().split('|')
    arr = arr.filter((item) => item !== domain)
    $('#id_demanded_domains').val(arr[0])
    arr.forEach(function (item, index) {
        if (index !== 0) {
            let val = $('#id_demanded_domains').val()
            $('#id_demanded_domains').val(val.concat('|', item))
        }
    })
}
