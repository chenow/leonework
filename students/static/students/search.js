$(document).ready(function () {
    update_companies()
})

function update_companies() {
    $('#company_list').html('')
    let encadrement = ''
    if ($('input[name="encadrement"]:checked').length !== 0) {
        encadrement = $('input[name="encadrement"]:checked')[0].value
        $.each($('input[name="encadrement"]:checked'), function () {
            if (!(encadrement === $(this).val())) {
                encadrement += ',' + $(this).val()
            }
        })
    } else {
        encadrement = 'none'
    }
    axios
        .get(`get/entreprise_card`, {
            params: {
                matchingOndomaine: $('#matchingOndomaine').is(':checked'),
                matchingOnWeekend: $(
                    'input[name="travail_wekeend"]:checked'
                ).val(),
                matchingOnEncadrement: encadrement,
                matchingOnteleworking: $(
                    'input[name="teleworking"]:checked'
                ).val(),
                matchingOnDepartement: $('#matchingOnDepartement').is(
                    ':checked'
                ),
                DateDebutMission: $('input[name="beginning_date"]').val(),
                DateFinMission: $('input[name="ending_date"]').val(),
            },
        })
        .then(function (response) {
            let jobsDenied = JSON.parse(
                localStorage.getItem('jobsDenied') || '{"jobs":[]}'
            )
            response.data.forEach((company, index) => {
                if (!jobsDenied.jobs.includes(company['id'])) {
                    let company_values_html = build_valeurs_companies(
                        company['company_values']
                    )
                    let heart = build_heart_search(company)
                    if (index % 3 == 0) {
                        group = index
                        $('#company_list').append(
                            `<div id="group_${group}" class="row gx-3 mb-3"></div>`
                        )
                    }
                    $(`#group_${group}`).append(
                        generate_card(company, company_values_html, heart)
                    )
                }
            })
            create_like_animation()
        })
}
