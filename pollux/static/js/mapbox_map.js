//mapBox = heatMap.extend({

class mapBox extends heatMap {
//class mapBox {
    constructor(layers, options, mapbox_access_token) {
        super(layers, options, mapbox_access_token)
        L.mapbox.accessToken = mapbox_access_token;
        this.ID = 'mapbox';
    }

    init() {
        let mapboxTiles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=' + L.mapbox.accessToken, {
            attribution: '© <a href="https://www.mapbox.com/feedback/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            tileSize: 512,
            zoomOffset: -1
            });
        this.map = new L.mapbox.Map('city_map')
                        .setView([45.198848, 5.735703], 14)
                        .addLayer(mapboxTiles);

        this.loadJson()
        //this.createLayers()

        //var featureLayer = L.mapbox.featureLayer(data).addTo(map);
    }

    createLayer() {
        var layers_form = document.getElementById('layers');
        for (let layer of this.layers) {
            let div = layers_form.appendChild(document.createElement("div"));
            let input = div.appendChild(document.createElement("input"))
            input.type = 'checkbox';
            //input.onclick = 'showLayer();';
            input.innerText = layer.name;
        }
    }
}