
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

// Return facility description for infoWindow
function getFacilityInformation(serviceDesc, completeAddress, locationName, locationPhoto, isPhotoExist){
  var imageUrl;
  var completeDescription = '<b>'+locationName+'</b><br>'+ serviceDesc;

  // Check if location has a photo
  if (isPhotoExist == 1){
    completeDescription += '<br><img src="/img?img_id='+ locationPhoto +'" width=50% height=50% id="'+ locationPhoto +'">';
  }
  
  completeDescription += '<br><small>'+ completeAddress +'</small>';
  
  return completeDescription;
}

// Show a map centered at (position.coords.latitude, position.coords.longitude).
function showMap(position, zoomValue, mapElement){
  var map;
  var mapOptions = {
    center: new google.maps.LatLng(position.coords.latitude, position.coords.longitude),
    zoom: zoomValue,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };

  map = new google.maps.Map(document.getElementById(mapElement), mapOptions);
  
  return map;
}

// Marked on locations along with the info window
function showMarker(map, latitude, longitude, titleName, infoContent){
  var latLng = new google.maps.LatLng(latitude, longitude);
  var marker = new google.maps.Marker({
    position: latLng,
    map: map,
    title: titleName
  });
  
  var infoWindow = new google.maps.InfoWindow();
  
  google.maps.event.addListener(marker, 'click', (function setInfoWindow(marker){
    return function(){
      infoWindow.setPosition(latLng);
      infoWindow.setContent(infoContent);
      infoWindow.open(map, marker); 
    }    
  })(marker));
  
  return marker;
}

// Show location error
function displayError(positionError) {
  alert("Could not determine location.");
}


