$(document).ready(function () {
    update_matches()
})

function update_matches() {
    $('#matches').html('')
    axios.get(`/companies/get/matches`).then(function (response) {
        response.data.forEach((student, index) => {
            let heart = build_heart(student)
            let qualities = build_qualities(student['qualities'])

            group = index
            $('#matches').append(`
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
        })
        create_like_animation()
    })
}
