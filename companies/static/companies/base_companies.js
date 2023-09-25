function create_like(student_id) {
    axios.post(`/matching/likes/create_like/company/${student_id}/`)
}

function build_valeurs_companies(valeurs) {
    let company_values_html = new String()
    valeurs.forEach((valeur) => {
        company_values_html += `
          <div style='color: #f0645a'
               class="d-inline-block border text-center bold border-danger rounded-pill m-1 px-2 py-1">
            ${valeur}
          </div>`
    })
    return company_values_html
}

function create_like_animation() {
    let buttons = document.querySelectorAll('.heart')
    buttons.forEach((button) => {
        button.addEventListener('click', () => {
            if (button.classList.contains('liked')) {
                button.classList.remove('liked')
            } else {
                button.classList.add('like_animation')
                setTimeout(function () {
                    button.classList.remove('like_animation')
                    button.classList.add('liked')
                }, 1000)
            }
        })
    })
}

function build_heart(student) {
    let heart = new String()
    if (student['is_liked'] == false) {
        heart = `<button class="btn p-0 position-absolute end-0" onclick="create_like(${student['user_id']})"><div class="heart"></div></button>`
    } else {
        heart = `<button class="btn p-0 position-absolute end-0" onclick="create_like(${student['user_id']})"><div class="heart liked"></div></button>`
    }
    return heart
}

function build_heart_search(company) {
    let heart = new String()
    if (company['is_liked'] == false) {
        heart = `
    <div class="d-flex justify-content-between align-items-center">
      <a class="btn m-0 p-0" onclick="remove_card(${company['user_id']})">
        <i class="bi bi-x" style="font-size: 2.8em;"></i>
      </a>
      <button class="btn p-0 h-100 position-relative btn-lg" onclick="create_like(${company['user_id']})">
        <div class="heart"></div>
      </button>
    </div>`
    } else {
        heart = `<div class="d-flex justify-content-between align-items-center">
    <a class="btn m-0 p-0" onclick="remove_card(${company['user_id']})"><i class="bi bi-x" style="font-size: 2.8em;"></i></a>
    <button class="btn p-0 position-relative" onclick="create_like(${company['user_id']})"><div class="heart liked"></div></button>
       </div>`
    }
    return heart
}

function remove_card(student_id) {
    $(`#${student_id}`).html('')
    let studentsDenied = JSON.parse(
        localStorage.getItem('studentsDenied') || '{"students":[]}'
    )
    studentsDenied.students.push(student_id)
    localStorage.setItem('studentsDenied', JSON.stringify(studentsDenied))
}

function build_qualities(qualities) {
    let html = new String()
    qualities.forEach((qualite) => {
        html += `
    <div style='color: #f0645a'
         class="d-inline-block border text-center bold border-danger rounded-pill m-1 px-2 py-1">
      ${qualite}
    </div>`
    })
    return html
}

function build_postes(postes) {
    let html = ''
    postes.forEach((poste) => {
        html += `<p class="text-truncate m-0">${poste}</p>`
    })
    return html
}

function generate_card(student, heart, qualities, postes) {
    return `
  <div class="col-sm-4" id=${student['user_id']}>
      <div class="card ent-card h-100 shadow">
          <div class="card-body d-flex flex-column">
              <div class="card-title d-flex justify-content-between p-2">
                  <div class="col-lg-6">
                  <img class="rounded-pill img-fluid" src="${
                      student['photo']
                  }"></div>
                  <div class="col-lg-6 p-2">
                  <h6 class="bold text-center">
                  ${student['first_name']} ${student['last_name']}
                  </h6>
                  ${postes}
                  </div>
              </div>
              <div class="border-bottom pb-2"><span class="text-muted">${
                  student['contract_type']
              }</span></div>
              <div class="card-text pt-2 d-flex flex-column">
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-calendar-event" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Début ${
                          student['beginning_date']
                      } <br> Fin : ${student['ending_date']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-hourglass-split" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Rythme : ${
                          student['apprenticeship_rate']
                      }</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-building" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Ecole : ${student['school']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-trophy" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Diplôme en préparation :<br> ${
                          student['ongoing_degree']
                      }</div>
                  </div>
              </div>
              <div>${qualities}</div>
               <footer class="mt-auto pt-3 d-flex justify-content-between flex-row">
                    <a class="bold d-flex align-items-center" href="/companies/get/student/${
                        student['user_id']
                    }/">
                      <i class="bi bi-caret-right me-3">Voir la fiche</i>
                    </a>
                     <a class="btn m-0 p-0" onclick="remove_card(${
                         student['user_id']
                     })"><i class="bi bi-x" style="font-size: 2.8em;"></i>
                     </a>
                    <button class="btn p-0 position-relative" onclick="create_like(${
                        student['user_id']
                    })">
                        <div class="heart ${
                            student['is_liked'] ? 'liked' : ''
                        }"></div>
                    </button>
              </footer>
          </div>
      </div>
  </div>
        `
}

function generate_card_display(student, heart, qualities, postes) {
    return `
  <div class="col-sm-10" id=${student['user_id']}>
      <div class="card ent-card h-100 shadow">
          <div class="card-body d-flex flex-column">
              <div class="card-title d-flex justify-content-between p-2">
                  <div class="col-lg-6">
                  <img class="rounded-pill img-fluid" src="${
                      student['photo']
                  }"></div>
                  <div class="col-lg-6 p-2">
                  <h6 class="bold text-center">
                  ${student['first_name']} ${student['last_name']}
                  </h6>
                  ${postes}
                  </div>
              </div>
              <div class="border-bottom pb-2"><span class="text-muted">${
                  student['contract_type']
              }</span></div>
              <div class="card-text pt-2 d-flex flex-column">
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-calendar-event" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Début ${
                          student['beginning_date']
                      } <br> Fin : ${student['ending_date']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-hourglass-split" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Rythme : ${
                          student['apprenticeship_rate']
                      }</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-building" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Ecole : ${student['school']}</div>
                  </div>
                  <div class="row mb-2 w-100">
                      <div class="col-2 p-0 text-center"><i class="bi bi-trophy" style="font-size: 16px;"></i></div>
                      <div class="col-10 p-0">Diplôme en préparation :<br> ${
                          student['ongoing_degree']
                      }</div>
                  </div>
              </div>
              <div>${qualities}</div>
             <footer class="mt-auto pt-3 d-flex justify-content-between flex-row">
                    <a class="bold d-flex align-items-center" href="/companies/get/student/${
                        student['user_id']
                    }/">
                      <i class="bi bi-caret-right me-3">Voir la fiche</i>
                    </a>
                     <a class="btn m-0 p-0" onclick="remove_card(${
                         student['user_id']
                     })"><i class="bi bi-x" style="font-size: 2.8em;"></i>
                     </a>
                    <button class="btn p-0 position-relative" onclick="create_like(${
                        student['user_id']
                    })">
                        <div class="heart ${
                            student['is_liked'] ? 'liked' : ''
                        }"></div>
                    </button>
              </footer>
          </div>
      </div>
  </div>
        `
}
