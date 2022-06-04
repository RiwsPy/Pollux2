
function create_map(mapbox_access_token, data) {
    L.mapbox.accessToken = mapbox_access_token;
    var map = new L.mapbox.Map('city_map')
                    .setView([45.198848, 5.735703], 14)
                    .addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/streets-v11'));

    var featureLayer = L.mapbox.featureLayer(data).addTo(map);
}
