// Function to intialize and add map
function initMap() {
    // Retrieving dictionary of cafe's coordinates
    $.get('/cafe-coordinates', response => {

            // Creating variable for response dictionary
            const coordinates = response;

            // Displaying map in 'cafe_map' DIV on details.html
            map = new google.maps.Map(document.getElementById('cafe_map'), {

                // Setting center to cafe's coordinates, zoom
                center: {
                    lat: coordinates['latitude'],
                    lng: coordinates['longitude'],
                  },
				zoom: 13,
                mapId: '3a38d6b637efa469'
            });

                // Creating a map marker and setting it to a variable
                const mapMarker = new google.maps.Marker({
                    // Setting position based on coordinates from dictionary
                    position: {lat: coordinates["latitude"], lng: coordinates["longitude"]},
                    map,
                    title: "Cafe",
                });
                
                // Retrieving dictionary of cafes' information
                $.get('/cafe-marker', response => {

                    // Creating a variable for response dictionary
                    const markerInfo = response;

                    // Creating an info window and setting it to a variable
                    const infowindow = new google.maps.InfoWindow ({
                        // Including name and address
                        content: "<p>" + markerInfo[0][0] + "</p><p>" + markerInfo[0][2] + "<br>" 
                        + markerInfo[0][3] + ", " + markerInfo[0][4] + " " + markerInfo[0][5] + "</p>",
                    });

                    // Listening for click of marker on map
                    mapMarker.addListener("click", () => {
                        // Show info window
                        infowindow.open(map, mapMarker);
                    });
                });
    });
}