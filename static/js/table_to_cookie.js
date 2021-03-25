function saveTableDataToCookie(api) {
  console.log("I am saving table data to csv");
  var tableData = new Array();
  table = document.getElementById(`tableData-${api}`);
  console.log(table);
  for (var row = 0; row < table.rows.length; row++) {
    var r = new Array();
    for (var col = 0; col < table.rows[row].cells.length; col++) {
      r.push(table.rows[row].cells[col].innerText);
    }
    tableData.push(r);
  }

  function createCookie(name, value, days) {
    var expires;
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
      expires = "; expires=" + date.toGMTString();
    } else {
      expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
  }

  function getCookie(c_name) {
    if (document.cookie.length > 0) {
      c_start = document.cookie.indexOf(c_name + "=");
      if (c_start != -1) {
        c_start = c_start + c_name.length + 1;
        c_end = document.cookie.indexOf(";", c_start);
        if (c_end == -1) {
          c_end = document.cookie.length;
        }
        return unescape(document.cookie.substring(c_start, c_end));
      }
    }
    return "";
  }

  var json_str = JSON.stringify(tableData);
  createCookie("mycookie", json_str);
}
