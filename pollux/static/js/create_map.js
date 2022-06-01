// require clsMap.js

function create_map(fileLayer, options, ID) {
    new heatMap(fileLayer, options, ID);
}

function create_map_recommandation(fileLayer, options) {
    new recommendationMap(fileLayer, options);
}
