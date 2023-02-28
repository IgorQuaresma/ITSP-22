///map options
let mapOptions = {
    center:[47.9990, 7.8421],
    zoom: 13}

// define the map
var map = L.map('map', mapOptions)

// include tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// marker to mark center of the city
var marker = L.marker([47.9990, 7.8421]).addTo(map);


// Add a button to the HTML page and add a get the user location when clicked
function showUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            var userMarker = L.marker([latitude, longitude]).addTo(map);
            map.setView([latitude, longitude], 13);
        });
    }
}

var userLocationBtn = document.createElement('li');
userLocationBtn.innerHTML = '<span>Show my location</span>';
userLocationBtn.onclick = showUserLocation;
document.getElementById('user-location-btn').appendChild(userLocationBtn);