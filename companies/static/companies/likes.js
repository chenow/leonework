$(document).ready(function () {
    update_likes()
    update_ent_likes()
})

function update_likes() {
    $('#likes').html('')
    axios.get(`/companies/get/likes`).then(function (response) {
        let studentsDenied = JSON.parse(
            localStorage.getItem('studentsDenied') || '{"students":[]}'
        )
        response.data.forEach((student, index) => {
            if (!studentsDenied.students.includes(student['user_id'])) {
                let heart = build_heart_search(student)
                let qualities = build_qualities(student['qualities'])
                group = index
                $('#likes').append(`
          <div class="carousel-item">
              <div id="group_${group}" class="d-flex justify-content-evenly">
              </div>
          </div>
          `)

                $('#group_0').parent().addClass('active')
                $(`#group_${group}`).append(
                    generate_card_display(
                        student,
                        heart,
                        qualities,
                        build_postes(student['demanded_jobs'])
                    )
                )
            }
        })
        create_like_animation()
        if (response.data.length == 0) {
            $('#likes').html(
                "<div class='text-muted d-flex justify-content-center text-center'><p style='max-width: 50ch;'>Vous n'avez encore liké personne ! Cliquez sur le bouton coeur des profils correspondant à vos souhaits dans l'onglet 'mes companies'.</p></div>"
            )
        }
    })
}

function update_ent_likes() {
    $('#likes_students').html('')
    axios.get(`/companies/get/likes/students`).then(function (response) {
        let studentsDenied = JSON.parse(
            localStorage.getItem('studentsDenied') || '{"students":[]}'
        )
        response.data.forEach((student, index) => {
            if (!studentsDenied.students.includes(student['user_id'])) {
                let heart = build_heart_search(student)
                let qualities = build_qualities(student['qualities'])

                group = index
                $('#likes_students').append(`
          <div class="carousel-item">
              <div id="group_ent_${group}" class="d-flex justify-content-evenly">
              </div>
          </div>
          `)
                $('#group_ent_0').parent().addClass('active')
                $(`#group_ent_${group}`).append(
                    generate_card_display(
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
