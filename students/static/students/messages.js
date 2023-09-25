function get_chat(conversation, ent_pk) {
    $('.active_chat').map(function () {
        this.classList.remove('active_chat')
    })
    localStorage.setItem('company', ent_pk)
    conversation.addClass('active_chat')
    input = $('input[name="job_id"]')[0].value = ent_pk
    $('#messages').html('')
    axios
        .get(`/matching/messages/get/student/${ent_pk}/`)
        .then(function (response) {
            response.data.forEach((chat, index) => {
                if (chat[2] == 'student') {
                    $('#messages').append(`
          <div class="outgoing_msg">
          <div class="sent_msg">
              <p>${chat[0]}</p>
              <span class="time_date">${chat[1]}</span>
          </div>
      </div>
        `)
                } else {
                    $('#messages').append(`
            <div class="incoming_msg">
              <div class="incoming_msg_img">
                  <img src="https://ptetutorials.com/images/user-profile.png" alt="sunil" />
              </div>
              <div class="received_msg">
                  <div class="received_withd_msg">
                      <p>${chat[0]}</p>
                      <span class="time_date">${chat[1]}</span>
                  </div>
              </div>
            </div>
        `)
                }
            })
            $('#messages').scrollTop($('#messages')[0].scrollHeight)
        })
}

function update_card() {
    $('#card').html('')
    let job = $('input[name="job_id"]')[0].value
    axios
        .get(`/matching/messages/get/card/job/${job}`)
        .then(function (response) {
            response.data.forEach((company, index) => {
                let company_values_html = build_valeurs_companies(
                    company['company_values']
                )

                $('#card').append(
                    generate_card_messages(company, company_values_html)
                )
            })
        })
}

function send_message() {
    let job_pk = $('#job_id').val()
    let chat = $('#chat_id').val()
    if (chat === '') {
        return
    }
    $('#chat_id').val('')
    axios({
        method: 'post',
        url: 'send_message',
        data: {
            job_pk: job_pk,
            chat: chat,
        },
    }).then(function (response) {
        $('#messages').append(
            `
      <div class="outgoing_msg">
          <div class="sent_msg">
              <p>${chat}</p>
              <span class="time_date">A l'instant</span>
          </div>
      </div>`
        )
        $('#messages').scrollTop($('#messages')[0].scrollHeight)
        location.reload()
    })
}

$(document).ready(function () {
    if (localStorage.getItem('company') !== null) {
        let company = localStorage.getItem('company')
        get_chat($(`#cp_${company}`), company)
    }
})

function generate_card_messages(company, company_values_html) {
    return `
  <div class="card ent-card shadow">
      <div class="card-body d-flex flex-column">
          <div class="card-title d-flex justify-content-between p-2">
              <div class="col-lg-6">
              <img class="rounded-pill img-fluid" src="${company['photo']}"></div>
              <div class="col-lg-6 p-2">
              <h8 class="bold text-center"> ${company['last_name']}</h8>
              </div>
          </div>
          <div class="border-bottom pb-2"><span class="text-muted">${company['principal_activity']}</span></div>
          <div class="card-text pt-2 d-flex flex-column">
              <div class="row mb-2 w-100">
                  <div class="col-2 p-0 text-center"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-calendar-event" viewBox="0 0 16 16">
                  <path d="M11 6.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                  <path d="M3.5 0a.5.5 0 0 1 .5.5V1h8V.5a.5.5 0 0 1 1 0V1h1a2 2 0 0 1 2 2v11a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2h1V.5a.5.5 0 0 1 .5-.5zM1 4v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V4H1z"/>
                </svg></div>
                  <div class="col-10 p-0">Début ${company['beginning_date']} <br> Fin : ${company['ending_date']}</div>
              </div>
              <div class="row mb-2 w-100">
                  <div class="col-2 p-0 text-center"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-briefcase" viewBox="0 0 16 16">
                  <path d="M6.5 1A1.5 1.5 0 0 0 5 2.5V3H1.5A1.5 1.5 0 0 0 0 4.5v8A1.5 1.5 0 0 0 1.5 14h13a1.5 1.5 0 0 0 1.5-1.5v-8A1.5 1.5 0 0 0 14.5 3H11v-.5A1.5 1.5 0 0 0 9.5 1h-3zm0 1h3a.5.5 0 0 1 .5.5V3H6v-.5a.5.5 0 0 1 .5-.5zm1.886 6.914L15 7.151V12.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1-.5-.5V7.15l6.614 1.764a1.5 1.5 0 0 0 .772 0zM1.5 4h13a.5.5 0 0 1 .5.5v1.616L8.129 7.948a.5.5 0 0 1-.258 0L1 6.116V4.5a.5.5 0 0 1 .5-.5z"/>
                </svg></div>
                  <div class="col-10 p-0">
                  <div class="m-0">${company['proposed_job']}</div>
                  </div>
              </div>
              <div class="row mb-2 w-100">
                  <div class="col-2 p-0 text-center"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
                  <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A31.493 31.493 0 0 1 8 14.58a31.481 31.481 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94zM8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10z"/>
                  <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4zm0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"/>
                </svg></div>
                  <div class="col-10 p-0">Sur : ${company['cities']}</div>
              </div>
              <div>
                  ${company_values_html}
              </div>
          </div>
          <footer class="mt-auto pt-3 d-flex justify-content-between">
                        <a class="bold d-flex align-items-center" href="/students/get/company/${company['id']}/"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-caret-right" viewBox="0 0 16 16">
                        <path d="M6 12.796V3.204L11.481 8 6 12.796zm.659.753 5.48-4.796a1 1 0 0 0 0-1.506L6.66 2.451C6.011 1.885 5 2.345 5 3.204v9.592a1 1 0 0 0 1.659.753z"/>
                      </svg> voir la fiche</a>
                        <path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z"/>
                      </svg></button>
          </footer>
      </div>
  </div>
    `
}
