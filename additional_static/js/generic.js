!(function ($) {})(jQuery);

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

$.ajaxSetup({
  headers: {
    "X-CSRFToken": csrftoken,
  },
});

axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

$(function () {
  $("#datepicker").datepicker({
    changeMonth: true,
    changeYear: true,
    yearRange: "-80:+5",
    dateFormat: "dd/mm/yy",
  });

  $("#datepicker2").datepicker({
    changeMonth: true,
    changeYear: true,
    dateFormat: "dd/mm/yy",
  });
});
