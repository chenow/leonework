function update_values() {
    $('#id_company_values').val(company_values[0])
    company_values.forEach(function (item, index) {
        if (index !== 0) {
            let val = $('#id_company_values').val()
            $('#id_company_values').val(val.concat(',', item))
        }
    })
}

function remove_value(button) {
    company_values = company_values.filter(function (e) {
        return e !== button.getAttribute('value')
    })
    button.parentNode.remove()
    update_values()
}

function add_value(value) {
    if (company_values.length >= 5) {
        return
    }
    company_values.push(value)
    document.getElementById('values').innerHTML += `
        <div class="mx-2 mb-3 border rounded-pill py-2 px-3 d-flex">
            <span class='text-center'>${value}</span>
            <button type="button"
                    onclick="remove_value(this)"
                    value="${value}"
                    class="btn-close"
                    aria-label="Close"></button>
        </div>`
    update_values()
}

function changeColor(a) {
    if (a.classList.contains('logo_color')) {
        a.classList.remove('logo_color')
        company_values = company_values.filter(
            (e) => e !== a.getAttribute('value')
        )
        update_values()
        remove_value($(`button[value="${a.getAttribute('value')}"]`)[0])
    } else if (company_values.length >= 5) {
        return
    } else {
        a.classList.add('logo_color')
        add_value(a.getAttribute('value'))
    }
}
