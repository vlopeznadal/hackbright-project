function initMap() {
    $.get('/coordinate', response => {
            const coordinate = response;
            map = new google.maps.Map(document.getElementById('cafe_map'), {
                center: {
                    lat: coordinate['latitude'],
                    lng: coordinate['longitude'],
                  },
				zoom: 13,
                mapId: '3a38d6b637efa469'
            });

                const mapMarker = new google.maps.Marker({
                    position: {lat: coordinate["latitude"], lng: coordinate["longitude"]},
                    map,
                    title: "Cafe",
                });
                
                $.get('/marker', response => {
                    const markerInfo = response;
                    const infowindow = new google.maps.InfoWindow ({
                        content: "<p>" + markerInfo[0][0] + "</p><p>" + markerInfo[0][2] + "<br>" 
                        + markerInfo[0][3] + ", " + markerInfo[0][4] + " " + markerInfo[0][5] + "</p>",
                    });

                    mapMarker.addListener("click", () => {
                        infowindow.open(map, mapMarker);
                    });
                });
    });
}