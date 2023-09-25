$(document).ready(function () {
    update_matches()
})

function update_matches() {
    $('#matches').html('')
    axios.get('get/matches').then(function (response) {
        response.data.forEach((company, index) => {
            console.log(response.data)
            let company_values_html = build_valeurs_companies(
                company['company_values']
            )
            let heart = build_heart(company)
            group = index
            $('#matches').append(`
          <div class="carousel-item">
              <div id="group_${group}" class="d-flex justify-content-evenly">
              </div>
          </div>
          `)
            $('#group_0').parent().addClass('active')
            $(`#group_${group}`).append(
                generate_card_display(company, company_values_html, heart)
            )
        })
        create_like_animation()
    })
}
