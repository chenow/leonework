function studentComponent() {
    return {
        student_pk_conversation: localStorage.getItem('student'),
        get invoice_url() {
            return `/payment/invoice_request/${this.student_pk_conversation}/`
        },

        init() {
            if (this.student_pk_conversation) {
                handleConversationChange(this.student_pk_conversation)
            }
            this.$watch('student_pk_conversation', handleConversationChange)
        },
    }
}

function handleConversationChange(student_pk) {
    localStorage.setItem('student', student_pk)
    $('.active_chat').map(function () {
        this.classList.remove('active_chat')
    })
    $(`#student_${student_pk}`).addClass('active_chat')
    get_chat(student_pk)
    update_card(student_pk)
}

function get_chat(student_pk) {
    $('#messages').html('')
    axios
        .get(`/matching/messages/get/company/${student_pk}/`)
        .then(function (response) {
            response.data.forEach((chat, index) => {
                if (chat[2] == 'company') {
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

$(document).ready(function () {
    if (localStorage.getItem('student') !== null) {
        let student = localStorage.getItem('student')
        get_chat($(`#st_${student}`), student)
    }
})

function send_message() {
    let student_pk = $('#student_id').val()
    let chat = $('#chat_id').val()
    if (chat === '') {
        return
    }
    $('#chat_id').val('')
    axios({
        method: 'post',
        url: 'send_message',
        data: {
            student_pk: student_pk,
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
    })
    location.reload()
}

function update_card(student) {
    $('#card').html('')
    axios
        .get(`/matching/messages/get/card/student/${student}/`)
        .then(function (response) {
            response.data.forEach((student, index) => {
                let heart = build_heart(student)
                let qualities = build_qualities(student['qualities'])
                $('#card').append(
                    generate_card_messages(student, heart, qualities)
                )
            })
            create_like_animation()
        })
}

function generate_card_messages(student, heart, qualities) {
    return `
      <div class="card ent-card shadow">
          <div class="card-body d-flex flex-column">
              <div class="card-title d-flex justify-content-between p-2">
                  <div class="col-lg-6">
                  <img class="rounded-pill img-fluid" src="${student['photo']}"></div>
                  <h6 class="bold text-center col-lg-6 p-2">
                  ${student['first_name']} ${student['last_name']}
                  </h6>
              </div>
              <div class="border-bottom pb-2"><span class="text-muted">${student['contract_type']}</span></div>
              <div class="card-text pt-2 d-flex flex-column">
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-calendar-event" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Début ${student['beginning_date']} <br> Fin : ${student['ending_date']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-hourglass-split" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Rythme : ${student['apprenticeship_rate']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-building" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Ecole : ${student['school']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-trophy" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Diplôme en préparation :<br> ${student['ongoing_degree']}</div>
                  </div>
              </div>
              <div>${qualities}</div>
              <footer class="mt-auto pt-3 d-flex justify-content-between">
                            <a class="bold d-flex align-items-center" href="/companies/get/student/${student['user_id']}/"><i class="bi bi-caret-right" style="font-size: 16px;"></i>voir la fiche</a>
              </footer>
          </div>
      </div>
        `
}
