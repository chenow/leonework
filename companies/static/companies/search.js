$(document).ready(function () {
    update_companies()
})

function update_companies() {
    $('#student_list').html('')
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
        .get('/companies/get/student_card', {
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
            let studentsDenied = JSON.parse(
                localStorage.getItem('studentsDenied') || '{"students":[]}'
            )
            response.data.forEach((student, index) => {
                if (!studentsDenied.students.includes(student['user_id'])) {
                    let heart = build_heart_search(student, job_pk)
                    let qualities = build_qualities(student['qualities'])
                    if (index % 3 == 0) {
                        group = index
                        $('#student_list').append(
                            `<div id="group_${group}" class="row gx-3 mb-3"></div>`
                        )
                    }
                    $(`#group_${group}`).append(
                        generate_card(
                            student,
                            heart,
                            qualities,
                            build_postes(student['demanded_jobs'])
                        )
                    )
                }
            })
            create_like_animation()
        })
}
