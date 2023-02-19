///map options
let mapOptions = {
    center:[47.9990, 7.8421],
    zoom: 13}

var map = L.map('map', mapOptions)

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);


var marker = L.marker([47.9990, 7.8421]).addTo(map);

