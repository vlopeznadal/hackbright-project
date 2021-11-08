function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 44.9632328, lng: -93.2493657},
        zoom: 3,
        mapId: 'bf545e16b59f18e2'
    });

    new google.maps.Marker({
        position: myLatLng,
        map,
        title: "Marker",
    });
}