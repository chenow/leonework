function experiencesComponent(init_experience) {
    return {
        experiences: init_experience,
        get experiencesInput() {
            return this.experiences
                .map((experience) => {
                    return experience.join(',')
                })
                .join(';')
        },

        addExperience() {
            const type = $('#type').val()
            const ent = $('#ent').val()
            const duree = $('#duree').val()
            if (type && ent && duree) {
                this.experiences.push([type, ent, duree])
                $('#type').val("Choississez un type d'expérience")
                $('#ent').val('')
                $('#duree').val('')
            }
        },
    }
}

$(function () {
    var accentMap = {
        é: 'e',
        è: 'e',
    }
    var normalize = function (term) {
        var ret = ''
        for (var i = 0; i < term.length; i++) {
            ret += accentMap[term.charAt(i)] || term.charAt(i)
        }
        return ret
    }

    $('#ongoing_degree').autocomplete({
        source: function (request, response) {
            var matcher = new RegExp(
                $.ui.autocomplete.escapeRegex(request.term),
                'i'
            )
            response(
                $.grep(all_degrees, function (value) {
                    value = value.label || value.value || value
                    return matcher.test(value) || matcher.test(normalize(value))
                })
            )
        },
    })
})
