$(document).ready(function () {
    let max = 0
    $('.explanation').each((index, element) => {
        if (element.offsetHeight > max) {
            max = element.offsetHeight
        }
    })
    $('.explanation').each((index, element) => {
        element.style.height = max + 'px'
    })
})
