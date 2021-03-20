var user = "{{request.user}}";
var csrftoken = getToken("csrftoken");
var url = "/updateSoftware/";
var plan_form = document.getElementById("plan_form");
var download = document.getElementById('download')

var software_url  = document.getElementById('hidden_software_url').value
console.log(software_url)
// var indiamart_form = document.getElementById("indiamart_form");

console.log("This is software js script");

function getToken(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}


function fun(software_name) {
  var plan = plan_form.plan.value;

  if (plan == "") {
    alert("Please select your plan");
  } else {
    download.setAttribute('href',software_url)
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/Json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        plan: plan,
        software_name: software_name,
      }),
    })
      .then((response) => {
        console.log(response.json());
      })
      .then((data) => {
        console.log("Data", data);
      });
  }
}
