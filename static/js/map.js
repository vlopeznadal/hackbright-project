function initMap() {
    $.get('/coordinates', response => {
            const coordinates = response;
            map = new google.maps.Map(document.getElementById('map'), {
                center: {lat: coordinates[1]["latitude"], lng: coordinates[1]["longitude"]},
                zoom: 13,
                mapId: 'bf545e16b59f18e2'
            });

            for (const marker in coordinates) {
                const mapMarker = new google.maps.Marker({
                    position: {lat: coordinates[marker]["latitude"], lng: coordinates[marker]["longitude"]},
                    map,
                    title: "Cafe" + marker,
                    icon: {
                        url: "/static/img/markers/marker-" + marker + ".svg",
                        scaledSize: new google.maps.Size(38, 31)
                    }
                });
                $.get('/markers', response => {
                    const markerInfo = response;
                    const infowindow = new google.maps.InfoWindow ({
                        content: "<a href='cafes/"+ markerInfo[marker][1]+"'>" + markerInfo[marker][0] + "</a>",
                    });

                    mapMarker.addListener("click", () => {
                        infowindow.open(map, mapMarker);
                    });
                });
            }
    });
}