// require clsMap.js

function create_map(fileLayer, options, ID) {
    let map = new heatMap(fileLayer, options, ID);
    map.init()
}

function create_map_recommandation(fileLayer, options) {
    new recommendationMap(fileLayer, options);
}

function create_mapbox(fileLayer, options, mapbox_access_token) {
    let map = new mapBox(fileLayer, options, mapbox_access_token);
    map.init()
}
