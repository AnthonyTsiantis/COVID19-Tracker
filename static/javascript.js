function initMap() {
  if (navigator.geolocation){
    let giveUp = 1000 * 30;
    let tooOld = 1000 * 60 * 60;

    options = {
      enableHighAccuracy: true,
      timeout: giveUp,
      maximumAge: tooOld
    };

    navigator.geolocation.getCurrentPosition(onSucess, onError, options);
  } else {
    console.log("Not Supported");
  }
}

function onSucess(position) {
  const {latitude, longitude} = position.coords;
  var location = {lat: latitude, lng: longitude};
  var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 13, center: location});
  var marker = new google.maps.Marker({position: location, map: map});
  
  var API_KEY = "Your API key"; // Enter API key here
  
  let url = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${API_KEY}`;

  async function getData() {
    const response = await fetch(url);
    const data = await response.json();
    var state = data["results"][8]["address_components"][0]["long_name"];
    var country = data["results"][8]["address_components"][1]["long_name"];
    var loco = {
      state: state,
      country: country
    };
    console.log("Location obtained");
    fetch(`${window.origin}/`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(loco),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
    .then(function (response) {
      if (response.status !== 200) {
        console.log(`Response status was not 200: ${response.status}`);
        return ;
      } else {
        console.log("POST request sent please refresh your webpage");
        alert("POST request sent please refresh your webpage if you can not view local data");
      }
    });
  }
  getData();
}

function onError(error) {
  console.log(error);
}

function positive() {
  alert("You have tested positive for COVID-19. Quarantine immediately and wait patiently for further instructions from your healthcare provider.");
}