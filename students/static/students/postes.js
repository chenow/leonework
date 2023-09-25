function search_metiers() {
    search = $('#search_metiers').val()

    if (search == '') {
        return
    }
    $('#metiers_found').empty()
    $('#metiers_found').html('Chargement...')
    axios({
        url: `/metiers/pole_api/search_metiers/${search}`,
        method: 'get',
    }).then(function (response) {
        $('#metiers_found').empty()
        for (metier in response.data) {
            $('#metiers_found').after(
                `<li>${response.data[metier].libelle}</li>`
            )
        }
    })
}

$(function () {
    $('#metiers').autocomplete({
        source: metiers,
    })
    $('#domaines').autocomplete({
        source: domaines,
    })
})
