// Function to intialize and add map
function initMap() {
    // Retrieving dictionary of cafes' coordinates
    $.get('/results-coordinates', response => {

            // Creating variable for response dictionary
            const coordinates = response;

            // Displaying map in 'map' DIV on results.html
            map = new google.maps.Map(document.getElementById('map'), {

                // Setting center and zoom to 0; Using bounds to set dependent on markers
                center: new google.maps.LatLng(0, 0),
				zoom: 0,
                mapId: 'bf545e16b59f18e2'
            });
            // Creating a list of the marker bounds objects
            const LatLngList = [];
            // For each set of coordinates in the dictionary (keys are numbers)
            for (const marker in coordinates) {
                // Adding marker bounds object into list using latitude and longitudes from dictionary
                LatLngList.push(new google.maps.LatLng (coordinates[marker]["latitude"],coordinates[marker]["longitude"]));

                // Creating a map marker and setting it to a variable
                const mapMarker = new google.maps.Marker({
                    // Setting position based on coordinates from dictionary
                    position: {lat: coordinates[marker]["latitude"], lng: coordinates[marker]["longitude"]},
                    map,
                    title: "Cafe" + marker,
                    // Customizing markers with svgs and setting size
                    icon: {
                        url: "/static/img/markers/marker-" + marker + ".svg",
                        scaledSize: new google.maps.Size(38, 31)
                    }
                });
                
                // Retrieving dictionary of cafes' information
                $.get('/results-markers', response => {

                    // Creating a variable for response dictionary
                    const markerInfo = response;

                    // Creating an info window and setting it to a variable
                    const infowindow = new google.maps.InfoWindow ({
                        // Including a linked name and address
                        content: "<p><a href='cafes/"+ markerInfo[marker][1]+"'>" + markerInfo[marker][0] + "</a></p><p>" + markerInfo[marker][2] + "<br>" 
                        + markerInfo[marker][3] + ", " + markerInfo[marker][4] + " " + markerInfo[marker][5] + "</p>",
                    });

                    // Listening for click of marker on map
                    mapMarker.addListener("click", () => {
                        // Show info window
                        infowindow.open(map, mapMarker);
                    });
                });

                // Creating map bounds object and setting it to a variable
                const bounds = new google.maps.LatLngBounds ();

                // For each marker bounds object in list
                for (let i = 0, LtLgLen = LatLngList.length; i < LtLgLen; i++) {
                    // Extend bounds object for specific marker
                    bounds.extend(LatLngList[i]);
                }

                // Fit map to specified bounds
                map.fitBounds(bounds);
            }
    });
}