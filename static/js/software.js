var user = "{{request.user}}";
var csrftoken = getToken("csrftoken");
var url = "/updateSoftware/";
var plan_form = document.getElementById("plan_form");
var reseller = document.getElementById("reseller_id");
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

console.log(reseller);

function fun(software_name) {
  var plan = plan_form.plan.value;
  var resellerText = reseller.value;
  if (plan == "" || resellerText === "") {
    alert("Please select your plan and reseller id ");
  } else {
    console.log("raweraewurier", resellerText, typeof resellerText);
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/Json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({
        plan: plan,
        software_name: software_name,
        reseller: resellerText,
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
