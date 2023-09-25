function changeColorLanguage(a) {
    if (a.classList.contains('logo_color')) {
        a.classList.remove('logo_color')
        spoken_languages = spoken_languages.filter(
            (e) => e !== a.getAttribute('language')
        )
        update_langue()
        remove_langue($(`button[language="${a.getAttribute('language')}"]`)[0])
    } else if (spoken_languages.length >= 5) {
        return
    } else {
        a.classList.add('logo_color')
        add_langue(a.getAttribute('language'))
    }
}

function add_langue(language) {
    spoken_languages.push([language, 'débutant'])
    document.getElementById('languages').innerHTML += `
    <div id="chosen_${language}"
         class="mx-2 mb-3 container-fluid border rounded-pill py-2 px-3">
        <div class="row">
            <div class="col-11">
                <span class='text-center violine'><b>${language}</b></span>
                <select onchange='add_language_level(${language}, this.options[this.selectedIndex].value)'
                        class="form-select"
                        aria-label="Niveau de language">
                    <option value="debutant" selected>
                        Débutant
                    </option>
                    <option value="intermediaire"
                            >
                        Intermédiaire
                    </option>
                    <option value="avancee">
                        Avancé
                    </option>
                    <option value="bilingue">
                        Bilingue
                    </option>
                </select>
            </div>
            <div class="col-1 align-items-center">
                <button type="button"
                        onclick="remove_lang('{{ lang }}')"
                        class="btn-close"
                        aria-label="Close">
                </button>
            </div>
        </div>
    </div>
    `

    update_spoken_languages()
}

function update_spoken_languages() {
    if (spoken_languages.length == 0) {
        $('#id_spoken_languages').val('')
        return
    }
    $('#id_spoken_languages').val(spoken_languages[0])
    spoken_languages.forEach(function (item, index) {
        if (index !== 0) {
            let val = $('#id_spoken_languages').val()
            $('#id_spoken_languages').val(val.concat('|', item))
        }
    })
}

function remove_lang(language) {
    $(`[id="chosen_${language}"]`).remove()
    spoken_languages = spoken_languages.filter((item) => item[0] !== language)
    update_spoken_languages()
}

function update_qualities() {
    $('#id_qualities').val(qualities[0])
    qualities.forEach(function (item, index) {
        if (index !== 0) {
            let val = $('#id_qualities').val()
            $('#id_qualities').val(val.concat(',', item))
        }
    })
}

function remove_qualite(button) {
    qualities = qualities.filter(function (e) {
        return e !== button.getAttribute('quality')
    })
    button.parentNode.remove()
    update_qualities()
}

function add_qualite(quality) {
    qualities.push(quality)
    document.getElementById('qualities').innerHTML += `
          <div class="mx-2 mb-3 border rounded-pill py-2 px-3 d-flex">
              <span class='text-center'>${quality}</span>
              <button type="button"
                      onclick="remove_qualite(this)"
                      quality="${quality}"
                      class="btn-close"
                      aria-label="Close"></button>
          </div>`
    update_qualities()
}

function changeColorQualite(a) {
    if (a.classList.contains('logo_color')) {
        a.classList.remove('logo_color')
        qualities = qualities.filter((e) => e !== a.getAttribute('quality'))
        update_qualities()
        remove_qualite($(`button[quality="${a.getAttribute('quality')}"]`)[0])
    } else if (qualities.length >= 5) {
        return
    } else {
        a.classList.add('logo_color')
        add_qualite(a.getAttribute('quality'))
    }
}

function add_language_level(language, level) {
    spoken_languages.forEach(function (item, index) {
        if (item[0] == language) {
            spoken_languages[index][1] = level
        }
    })
    update_spoken_languages()
}
