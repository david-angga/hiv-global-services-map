
/*
  List of javascript helpers
*/


// Set input fields
function setInputFields(inputId, inputValue){
  var inputField = document.getElementById(inputId);

  if (inputField != null){
    inputField.value = inputValue;
  }
}

// Set drop down list value
function setDropDownListValue(ddlid, value){
  var ddl = document.getElementById(ddlid);
  
  if(ddl != null){
    for(var i=0; i < ddl.options.length ; i++){
      if(ddl.options[i].value === value){
        ddl.options[i].selected = 1;
      }
    }
  }
}

// Set toggle display
// toggle: 'on' , 'off'
function setToggle(elementId, toggle){
  if(toggle === 'on'){
    document.getElementById(elementId).style.display = 'inline';
  } else {
    document.getElementById(elementId).style.display = 'none';
  }
}

// Link to map page
function goToMapPage(){
  window.location.href = 'http://' + window.location.host + '/';
}

// Get response from theUrl
function httpGet(theUrl){
  var http = null;

  http = new XMLHttpRequest();
  http.open("GET", theUrl, false);
  http.send();
  
  return http.responseText;
}

