var searchBar = document.getElementById('search-bar');
var autocomplete = new google.maps.places.Autocomplete(searchBar);

navigator.geolocation.getCurrentPosition(function(position) {
    var userCoords = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
    };
});