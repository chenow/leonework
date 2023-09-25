$(document).ready(function () {
    update_ent_likes()
    update_likes()
})

function update_likes() {
    $('#likes').html('')
    axios.get('get/likes').then(function (response) {
        let jobsDenied = JSON.parse(
            localStorage.getItem('jobsDenied') || '{"jobs":[]}'
        )
        response.data.forEach((company, index) => {
            if (!jobsDenied.jobs.includes(company['id'])) {
                let company_values_html = build_valeurs_companies(
                    company['company_values']
                )
                let heart = build_heart_search(company)
                group = index
                $('#likes').append(`
                <div class="carousel-item">
                    <div id="group_${group}" class="d-flex justify-content-evenly">
                    </div>
                </div>
        `)
                $('#group_0').parent().addClass('active')
                $(`#group_${group}`).append(
                    generate_card_display(company, company_values_html, heart)
                )
            }
        })
        create_like_animation()
        if (response.data.length == 0) {
            $('#likes').html(
                "<div class='text-muted d-flex justify-content-center text-center'><p style='max-width: 50ch;'>Vous n'avez encore liké personne ! Cliquez sur le bouton coeur des profils correspondant à vos souhaits dans l'onglet 'mes entreprises'.</p></div>"
            )
        }
    })
}

function update_ent_likes() {
    $('#likes_ent').html('')
    axios.get('get/likes/ent').then(function (response) {
        let jobsDenied = JSON.parse(
            localStorage.getItem('jobsDenied') || '{"jobs":[]}'
        )
        response.data.forEach((company, index) => {
            if (!jobsDenied.jobs.includes(company['id'])) {
                let company_values_html = build_valeurs_companies(
                    company['company_values']
                )
                let heart = build_heart_search(company)

                group = index
                $('#likes_ent').append(`
        <div class="carousel-item">
            <div id="group_ent_${group}" class="d-flex justify-content-evenly">
            </div>
        </div>
        `)
                $('#group_ent_0').parent().addClass('active')
                $(`#group_ent_${group}`).append(
                    generate_card_display(company, company_values_html, heart)
                )
            }
        })
        create_like_animation()
    })
}
