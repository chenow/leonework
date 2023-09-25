function changeColor(a) {
    if (a.classList.contains('logo_color')) {
        a.classList.remove('logo_color')
        valeurs = valeurs.filter((e) => e !== a.getAttribute('valeur'))
    } else if (valeurs.length >= 5) {
        return
    } else {
        a.classList.add('logo_color')
        valeurs.push(a.getAttribute('valeur'))
    }
}

function get_valeurs() {
    axios({
        url: '/students/registration/atouts/get_valeurs',
        method: 'get',
    }).then(function (response) {
        $('#valeurs_liste').html(response.data)
    })
}

function save_valeurs() {
    axios({
        url: '/students/registration/atouts/valeurs',
        method: 'post',
        data: {
            valeurs: valeurs,
        },
    }).then(function (response) {
        get_valeurs()
    })
}

$(function () {
    $('#cities').autocomplete({
        source: cities,
        select: function (event, ui) {
            add_ville(ui.item.value)
            return false
        },
    })
})

function get_cities() {
    axios({
        url: '/students/registration/company/get_cities',
        method: 'get',
    }).then(function (response) {
        $('#liste_cities').html(response.data)
    })
}

function add_ville(city) {
    if (chosen_cities.lenght > 4) {
        return
    }
    if (!cities.includes(city)) {
        return
    }

    if (chosen_cities.includes(city)) {
        return
    }

    chosen_cities.push(city)
    axios({
        url: '/students/registration/company/save_cities',
        method: 'post',
        data: {
            cities: chosen_cities,
        },
    }).then(function (response) {
        get_cities()
    })
    $('#cities').val('')
}

function remove_ville(city) {
    chosen_cities = chosen_cities.filter(function (e) {
        return e !== city
    })
    axios({
        url: '/students/registration/company/save_cities',
        method: 'post',
        data: {
            cities: chosen_cities,
        },
    }).then(function (response) {
        get_cities()
    })
}

function remove_valeur(valeur) {
    valeurs = valeurs.filter(function (e) {
        return e !== valeur
    })
    save_valeurs()
}

$(document).ready(function () {
    get_valeurs()
    get_cities()
})
