function changeColor(a) {
    if (a.classList.contains('logo_color')) {
        a.classList.remove('logo_color')
        remove_value(a.getAttribute('valeur'))
    } else if (company_values.length >= 5) {
        return
    } else {
        a.classList.add('logo_color')
        add_value(a.getAttribute('valeur'))
    }
}

$(function () {
    $('#cities').autocomplete({
        source: cities,
        select: function (event, ui) {
            add_city(ui.item.value)
            return false
        },
    })
})

function add_city(city) {
    if (chosen_cities.includes(city)) {
        return
    }
    chosen_cities.push(city)
    $('#id_company_locations').val(chosen_cities.join(','))

    $('#cities_list').append(
        `<div class="mx-2 mb-3 border rounded-pill py-2 px-3 d-flex"
             id="${city}">
            <span class='text-center'>${city}</span>
            <button type="button"
                    onclick="remove_city('${city}')"
                    class="btn-close"
                    aria-label="Close"></button>
        </div>`
    )
}

function remove_city(city) {
    chosen_cities = chosen_cities.filter((e) => e !== city)
    $('#id_company_locations').val(chosen_cities.join(','))
    $(`#${city}`).remove()
}

function add_value(value) {
    if (company_values.includes(value)) {
        return
    }
    if (company_values.length >= 5) {
        return
    }
    if (value === null) {
        return
    }
    company_values.push(value)
    $('#id_company_values').val(company_values.join(','))
    $('#values_list').append(`
        <div
            class="mx-2 mb-3 border rounded-pill py-2 px-3 d-flex"
            id="${value}"
        >
            <span class="text-center">${value}</span>
            <button
                type="button"
                onclick="remove_value(this)"
                value="${value}"
                class="btn-close"
                aria-label="Close"
            ></button>
        </div>`)
}

function remove_value(button) {
    value = button.getAttribute('value')
    company_values = company_values.filter((e) => e !== value)
    $('#id_company_values').val(company_values.join(','))
    to_remove = button.parentNode
    to_remove.parentNode.removeChild(to_remove)
}
