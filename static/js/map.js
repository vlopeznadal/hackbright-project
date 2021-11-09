function initMap() {
    $.get('/coordinates', response => {
            const coordinates = response;
            map = new google.maps.Map(document.getElementById('map'), {
                center: new google.maps.LatLng(0, 0),
				zoom: 0,
                mapId: 'bf545e16b59f18e2'
            });

            const LatLngList = [];
            for (const marker in coordinates) {
                LatLngList.push(new google.maps.LatLng (coordinates[marker]["latitude"],coordinates[marker]["longitude"]));
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
                        content: "<p><a href='cafes/"+ markerInfo[marker][1]+"'>" + markerInfo[marker][0] + "</a></p><p>" + markerInfo[marker][2] + "<br>" 
                        + markerInfo[marker][3] + ", " + markerInfo[marker][4] + " " + markerInfo[marker][5] + "</p>",
                    });

                    mapMarker.addListener("click", () => {
                        infowindow.open(map, mapMarker);
                    });
                });

                const bounds = new google.maps.LatLngBounds ();
                for (let i = 0, LtLgLen = LatLngList.length; i < LtLgLen; i++) {
                    bounds.extend (LatLngList[i]);
                }
                map.fitBounds (bounds);
            }
            console.log(LatLngList);
    });
}