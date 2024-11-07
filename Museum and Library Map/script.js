// Function to prompt user for Google Maps API Key
function promptForApiKey() {
    let apiKey;
    while (!apiKey) {
        apiKey = prompt("Please enter your Google Maps API Key: ");
        if (!apiKey) {
            alert("You must enter a Google Maps API Key to use this site.");
        }
    }
    return apiKey;
}

// Prompt user for Google Maps API Key
const apiKey = promptForApiKey();
const script = document.createElement('script');
script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=places&callback=initializeMap`;
document.body.appendChild(script);

// Initialize variables
var locations = [], map;

// Define a Location class
class Location {
    constructor(name, town, latitude, longitude, type) {
        this.name = name;
        this.town = town;
        this.latitude = latitude;
        this.longitude = longitude;
        this.type = type;
    }
}

// Gets and sets all the locations from the Data NS Map for a given type (museum or library)
function setLocations(dataURL, iconURL, type) {
    $.ajax({
        url: dataURL,
        success: function(result) {
            // Checks what type of building each item is before pulling its data and creating a Location object for it
            // in the locations array.
            result.forEach(item => {
                var lat, lng;
                if (type == 'museum' && item.geolocation) {
                    lat = item.geolocation.coordinates[1];
                    lng = item.geolocation.coordinates[0];
                } else if (type == 'library' && item.location) {
                    lat = parseFloat(item.location.latitude);
                    lng = parseFloat(item.location.longitude);
                } else {
                    console.log(`Location data is missing for ${item.name}.`);
                    return;
                }

                var location = new Location(item.site || item.name, item.town || item.city, lat, lng, type);
                locations.push(location);
            });

            // Calls the setMarkers function
            setMarkers(iconURL, type);
        }
    });
}

// Sets all the markers of a given type (museum or library) onto the map, using the filled locations array
function setMarkers(iconURL, type) {
    // Create the icon for the building type
    var icon = {
        url: iconURL,
        scaledSize: new google.maps.Size(30, 30)
    };

    // Set the appropriate markers using the locations data
    locations.filter(location => location.type === type).forEach(location => {
        // Marker info
        const infowindow = new google.maps.InfoWindow({
            content: `<p style='color: black;'>${location.name},<br>${location.town}</p>`
        });

        // Create marker icon
        var marker = new google.maps.Marker({
            position: { lat: location.latitude, lng: location.longitude },
            icon: icon,
            animation: google.maps.Animation.DROP
        });

        // Show info when marker clicked
        marker.addListener("click", () => {
            infowindow.open({ anchor: marker, map });
        });

        // Set the marker on the map
        marker.setMap(map);
    });
}

// Initialize the map and its autocompleter
    // Will be called once Google Maps API is loaded (see line 4 callback)
function initializeMap() {
    // Load the map graphic
    var mapProperties = {
        center: new google.maps.LatLng(45.0000, -63.2000),
        zoom: 7
    };
    map = new google.maps.Map(document.getElementById("googleMap"), mapProperties);

    // Create an autocomplete object to aid user with queries and validate them
    var input = document.getElementById('searchInput');
    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    // Restrict the autocomplete results to Canada (can only restrict by country)
    autocomplete.setComponentRestrictions({
        country: 'CA'
    });

    // Set up a listener for the place_changed event to track when the user is making queries
    // and provide suggestions
    autocomplete.addListener('place_changed', function() {
        // Gets a place from the autocomplete suggestions when the user clicks it
        var place = autocomplete.getPlace();

        // Make sure the chosen place has valid info
        if (!place.geometry) {
            window.alert("No details available for input: '" + place.name + "'");
        } else {
            // If the place has a viewport, use it to set the map bounds
            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                // Otherwise, set the map center to the chosen place with static zoom
                map.setCenter(place.geometry.location);
                map.setZoom(10);
            }
        }
    });

    // Get and set Museum markers
    setLocations(
        "https://data.novascotia.ca/resource/f84a-3hfv.json",
        'museum_icon.png',
        'museum'
    );

    // Get and set Library markers
    setLocations(
        "https://data.novascotia.ca/resource/btmb-pp7q.json",
        'library_icon.png',
        'library'
    );
}