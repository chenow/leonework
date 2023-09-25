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

function build_heart(company) {
    let heart = new String()
    if (company['is_liked'] == false) {
        heart = `<button class="btn p-0 h-100 position-relative btn-lg" onclick="create_like(${company['id']})"><div class="heart"></div></button>
  `
    } else {
        heart = `
    <button class="btn p-0 position-relative" onclick="create_like(${company['id']})"><div class="heart liked"></div></button>`
    }
    return heart
}

function build_heart_search(company) {
    let heart = new String()
    if (company['is_liked'] == false) {
        heart = `
    <div class="d-flex justify-content-between">
      <a class="btn m-0 p-0" onclick="remove_card(${company['id']})">
        <i class="bi bi-x" style="font-size: 2.8em;"></i>
      </a>
      <button class="btn p-0 h-100 position-relative btn-lg" onclick="create_like(${company['id']})">
        <div class="heart"></div>
      </button>
    </div>`
    } else {
        heart = `
    <div class="d-flex justify-content-between">
      <a class="btn m-0 p-0" onclick="remove_card(${company['id']})">
        <i class="bi bi-x" style="font-size: 2.8em;"></i>
      </a>
      <button class="btn p-0 position-relative" onclick="create_like(${company['id']})">
        <div class="heart liked"></div>
      </button>
    </div>`
    }
    return heart
}
function remove_card(job_id) {
    $(`#${job_id}`).html('')
    let jobsDenied = JSON.parse(
        localStorage.getItem('jobsDenied') || '{"jobs":[]}'
    )
    jobsDenied.jobs.push(job_id)
    localStorage.setItem('jobsDenied', JSON.stringify(jobsDenied))
}

function generate_card(company, company_values_html, heart) {
    return `
<div class="col-sm-4" id="${company['id']}">
    <div class="card ent-card h-100 shadow">
        <div class="card-body d-flex flex-column">
            <div class="card-title d-flex justify-content-between p-2">
                <div class="col-lg-6">
                <img class="rounded-pill img-fluid" src="${company['photo']}"></div>
                <div class="col-lg-6 p-2">
                <h6 class="bold text-center">${company['name']}</h6>
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
                    <div class="col-10 p-0">Sur : ${company['job_location']}</div>
                </div>
                <div>
                    ${company_values_html}
                </div>
            </div>
            <footer class="mt-auto pt-3 d-flex justify-content-between flex-column">
              <div class="mb-3 w-100 text-muted">Date de publication : ${company['date_publication']}
              </div>
              <div class="mt-auto pt-3 d-flex">
                            <a class="bold d-flex align-items-center me-3" href="/students/get/company/${company['id']}/">
                              <i class="bi bi-caret-right">Voir la fiche</i>
                            </a>
                            ${heart}
              </div>
            </footer>
        </div>
    </div>
</div>
      `
}

function create_like(job_id) {
    axios.post(`/matching/likes/create_like/student/${job_id}/`)
}

function generate_card_display(company, company_values_html, heart) {
    return `
<div class="col-sm-10" id="${company['id']}">
    <div class="card ent-card h-100 shadow">
        <div class="card-body d-flex flex-column">
            <div class="card-title d-flex justify-content-between p-2">
                <div class="col-lg-6">
                <img class="rounded-pill img-fluid" src="${company['photo']}"></div>
                <div class="col-lg-6 p-2">
                <h6 class="bold text-center">${company['name']}</h6>
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
                    <div class="col-10 p-0">Sur : ${company['job_location']}</div>
                </div>
                <div>
                    ${company_values_html}
                </div>
            </div>
            <footer class="mt-auto pt-3 d-flex justify-content-between flex-column">
              <div class="mb-3 w-100 text-muted">Date de publication : ${company['date_publication']}
              </div>
              <div class="mt-auto pt-3 d-flex">
                            <a class="bold d-flex align-items-center me-3" href="/students/get/company/${company['id']}/">
                              <i class="bi bi-caret-right">Voir la fiche</i>
                            </a>
                            <a class="btn m-0 p-0" onclick="remove_card(${company['id']})">
        <i class="bi bi-x" style="font-size: 2.8em;"></i>
      </a>
                            ${heart}
              </div>
            </footer>
        </div>
    </div>
</div>
      `
}
