function defaultZonePos() {
    //return [[45.187501, 5.704696], [45.198848, 5.725703]];
    return [[45.15008475740563, 5.664997100830078], [45.221347171208436, 5.766019821166993]]
}

function defaultZoneBound() {
    return L.latLngBounds(defaultZonePos());
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


function addAttribution(map) {
    // choix à ajouter
    let tileLayer = L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        //'https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=XX', {
        //'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
        //'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 22,
            //attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
        }).addTo(map);
}


function addPopUp(feature, layer, invertIntensity) {
    if (feature.properties) {
        layer.bindPopup(generatePupUpContent(feature, invertIntensity) || 'Aucune donnée');
    }
}


function getIcon(feature, icon) {
    return L.icon({
        iconUrl: '../static/img/' + (icon || feature.icon || 'markers/default.png'),
        iconSize: [20, 20],
        });
}

function generatePupUpContent(feature, invertIntensity) {
    let content = '';
    // show full data
    for (let [k, v] of Object.entries(feature['properties'])) {
        if (k != 'pk') {
            content += addNewLineInContent(k, v)
        }
    }
    /*
    if (feature['properties']) {
        for (let [k, v] of Object.entries(feature['properties'])) {
            // TODO: les valeurs ne sont pas nécessairement maxées à 1, de quelle valeur faut-il faire la différence ?
            v = (invertIntensity  && k != 'Différence') ? 1- Math.min(v, 1): v,
            content += addNewLineInContent('Calque ' + k, v.toFixed(2), "0")
        }
    }
    */
    return content
}


function addNewLineInContent(category, content, default_value) {
    content = content || default_value;
    if (content) {
        return '<b>' + category + '</b>: ' + content + '<br>'
    }
    return ''
}


var defaultLegendColor = {
    0.15: 'violet',
    0.2:  'blue',
    0.4:  'lime',
    0.6:  'yellow',
    0.8:  'orange',
    1.0:  'red'
 };


class heatMap {
    /*
        options: {
            blur: 15,
            minOpacity: 0.05,
            legend: true,
            maxValueDefault: undefined,
            draw: true,
            gradient: {
                0.15: 'violet',
                0.2:  'blue',
                0.4:  'lime',
                0.6:  'yellow',
                0.8:  'orange',
                1.0:  'red'
             },
        },
    */
    constructor(layers, options) {
        this._options = {
            ...{
                blur: 15,
                minOpacity: 0.05,
                legend: {name: 'Légende'},
                draw: true,
                maxValueDefault: undefined,
                gradient: defaultLegendColor,
            },
            ...options
        };

        this._options.zoom.min = Math.min(this._options.zoom.min || 10, this._options.zoom.max || 20)
        this._options.zoom.max = Math.max(this._options.zoom.min, this._options.zoom.max || 20)
        this._options.zoom.init = Math.min(this._options.zoom.max,
                                    Math.max(this._options.zoom.min, this._options.zoom.init)
                                    )

        let params = window.location.href.split('/')
        this.invertIntensity = params[params.length - 1][0] == '-'

        this.layers = layers;
        this.init(false)
    }

    init(dontCreateMap, activeLayers) {
        for (let lyr of this.layers) {
            if (lyr.layerType == 'cluster') {
                let radius = function(zoom) {
                    return zoom >= 19? 1: 80;
                };
                lyr.layer = new L.markerClusterGroup({maxClusterRadius: radius});
            } else {
                lyr.layer = new L.FeatureGroup();
            }
            lyr.data = {};
        }

        this._DB = {};

        let controlLayers = this.createLayers();
        this.createMap(controlLayers, dontCreateMap, activeLayers);
        this.loadJson();

        // basic leaflet traduction
        document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
        document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
    }

    createLayers() {
        var controlLayers = {};
        if (this._options.draw) { // calque dessin
            this._drawLayer = new L.FeatureGroup();
            //controlLayers['Mon Calque'] = this._drawLayer;
        }
        for (let index in this.layers) {
            let fileData = this.layers[index]
            fileData = {
                ...this._options,
                ...fileData,
            }
            controlLayers[fileData.name] = fileData.layer
            this.layers[index] = fileData;
        };
        return controlLayers
    }

    createMap(controlLayers, dontCreateMap, activeLayers) {
        let bbox_lat_lng = defaultZoneBound()
        if (this._options.bbox) {
            bbox_lat_lng = L.latLngBounds([
                                [this._options.bbox[1],
                                this._options.bbox[0]],
                                [this._options.bbox[3],
                                this._options.bbox[2]]
                                ]);
        }

        activeLayers = activeLayers || [];
        if (activeLayers.length == 0 && this.layers) {
            for (let layer of this.layers) {
                if (layer.isActive) {
                    activeLayers.push(controlLayers[layer.name])
                    controlLayers[layer.name].isActive = true;
                }
            }
        }

        if (!dontCreateMap) {
            this.map = L.map('city_map', {
                    layers: activeLayers,
                    minZoom: this._options.zoom.min,
                    maxZoom: this._options.zoom.max,
                    wheelPxPerZoomLevel: this._options.wheelPxPerZoomLevel
                }).setView(bbox_lat_lng.getCenter(), this._options.zoom.init);
            this.map.owner = this;
        } else {
            this.map.setView(bbox_lat_lng.getCenter(), this._options.zoom.init);

            for (let layerName of activeLayers) {
                for (let layer in this.layers) {
                    if (this.layers[layer].name == layerName) {
                        this.map.addLayer(this.layers[layer].layer)
                        this.layers[layer].isActive = true;
                        break;
                    }
                }
            }
        }

        L.control.layers(null, controlLayers).addTo(this.map);

        if (!dontCreateMap) {
            addAttribution(this.map)

            if (this._options.buttons.fullScreen) {
                this.addFullScreenButton()
            }
            if (this._options.draw) {
                this.addDrawControl()
            }
            for (let [id, data] of Object.entries(this._options.buttons)) {
                if (data && id != 'fullScreen') {
                    this.map.addControl(new L.Control.MyButton({id: id, ...data}))
                }
            }
        }
    }

    addFullScreenButton() {
        this.map.addControl(new L.Control.Fullscreen({
            title: {
                'false': 'Vue plein écran',
                'true':  'Quitter le plein écran'
            }
        }));
    }

    addDrawControl() {
        this.map.addControl(
            new L.Control.Draw(
                this.drawOptions()
            ));
        this.update_map_on_click()
    }

    update_map_on_click() {
        let editableLayer = this._drawLayer;
        let map = this.map;
        let cls = this;

        map.on('overlayremove ', function(e) {
            for (let layer of cls.layers) {
                if (layer.name == e.name) {
                    layer.isActive = false;
                }
            }
            //console.log(map._active_layers)
        });

        map.on('overlayadd ', function(e) {
            for (let layer of cls.layers) {
                if (layer.name == e.name) {
                    layer.isActive = true;
                    break;
                }
            }

            //console.log(map._active_layers)
        });

        // create form
        map.on('draw:created', function(e) {
            cls.reload([
                e.layer._bounds._southWest.lng,
                e.layer._bounds._southWest.lat,
                e.layer._bounds._northEast.lng,
                e.layer._bounds._northEast.lat
            ])
        });
    }

    reload(bound) {
        let map = this.map;
        let activeLayers = [];
        let activeNbLayers = [];
        let nb = 0;
        for (let layer of this.layers) {
            if (layer.isActive) {
                activeLayers.push(layer.name)
                activeNbLayers.push(nb)
            }
            nb += 1;
        }

        window.location.href =
            '?zoom=' + this.map.getZoom() +
            '&layers=' +
            (activeNbLayers.join('/') || -1) +
            '&bound=' +
            bound[0].toFixed(6) + '/' +
            bound[1].toFixed(6) + '/' +
            bound[2].toFixed(6) + '/' +
            bound[3].toFixed(6);
    }

    addLegend(layer, maxValueInLayer) {
        // TODO: bug affichage légende quand une carte sans layer est chargée puis qu'un layer est ajouté
        if (!this._options.legend) {
            return;
        }

        if (this._legendDiv) {
            this._legendDiv.remove();
        }

        var legend = L.control({ position: "bottomright" });
        let legendBox = L.DomUtil.create("div", "legendBox");
        let legendName = L.DomUtil.create('h4', 'legendName', legendBox);
        legendName.textContent = this._options.legend.name;
        this._legendDiv = legendBox;

        if (maxValueInLayer) {
            this.updateLegend(layer, maxValueInLayer)
        }
        legend.onAdd = function(map) {
            return legendBox
        };
        legend.addTo(this.map);
    }

    updateLegend(layer, maxValue) {
        if (!this._options.legend || !this._options.gradient) {
            return;
        }

        if (layer) {
            this.showLegendDetails(maxValue)
        }
    }

    showLegendDetails(maxValue) {
        let i = 0;
        let maxValueInLegend = null;
        maxValue = maxValue || 1.0;
        for (let [legendValue, color] of Object.entries(this._options.gradient).sort().reverse()) {
            //let lineColor = L.DomUtil.create('i', 'legendButton_' + i, this._legendDiv);
            //lineColor.innerHTML += 'style="background: ' + color + ';"';
            //let lineText = L.DomUtil.create('span', 'legendValue_' + i, this._legendDiv);
            //lineText.textContent = value + '<br>';

            //if (maxValueInLegend == null) {
            //    maxValueInLegend = this._options.legend.max == undefined? legendValue: this._options.legend.max;
            //}
            maxValueInLegend = maxValueInLegend == undefined? legendValue: maxValueInLegend;
            this._legendDiv.innerHTML += '<i id="legendButton_' + i + '" style="background: ' + color + '"></i>'
            this._legendDiv.innerHTML += '<span>' + ' >= ' +
                                            '<span id="legendValue_' + i + '">' +
                                                (maxValue * legendValue / maxValueInLegend).toFixed(2) +
                                            '</span>' +
                                         '</span><br>'
            i += 1;
        }
    }

    loadJson(fileData) {
        var files_to_load = {};
        for (let layerdata of this.layers) {
            if (!(layerdata.filename in files_to_load)) {
                files_to_load[layerdata.filename] = true;
                this.request(layerdata, fileData);
            }
        };
    }

    request(layerdata) {
        let request = new Request('/api/' + layerdata.filename + '?bound=' + this._options.bbox, {
            //method: 'POST',
            method: 'GET',
            //body: JSON.stringify({bbox: this._options.bbox}),
            headers: new Headers({
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            })
        })
        fetch(request)
        .then((resp) => resp.json())
        .then((data) => {
            this._DB[layerdata.filename] = data;
            for (let layer of this.layers) {
                if (layer.filename == layerdata.filename) {
                    this.createLayer(layer);
                }
            }
        });
    }

    createLayer(layer) {
        if (layer.layerType == 'heatmap') {
            this.createHeatLayer(this._DB[layer.filename], layer)
        } else if (layer.layerType == 'node' || layer.layerType == 'cluster') {
            this.createNodeLayer(this._DB[layer.filename], layer)
        };
    }

    createNodeLayer(data, layer) {
        let cls = this;
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                let marker = L.marker(latlng, {icon: getIcon(layer),
                                               rotationAngle: cls.getOrientation(feature, layer)});
                addPopUp(feature, marker, cls.invertIntensity);
                return marker;
            }
        }).addTo(layer.layer);
    }

    heatLayerAttr(layer) {
        return {
                 ...this._options,
                 max: Math.min(1, Math.max(0, ...Object.keys(this._options.gradient))),
                 ...layer,
                }
    }

    createHeatLayer(data, layer) {
        let heatMapData = [];
        let cls = this;
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                let itm_intensity = d.properties[layer.value.field] || layer.value.fix || 0;
                if (layer.value.min) {
                    itm_intensity = Math.max(layer.value.min, itm_intensity)
                }
                if (layer.value.max) {
                    itm_intensity = Math.min(layer.value.max, itm_intensity)
                    if (layer.value.invert) {
                        itm_intensity = layer.value.max - itm_intensity;
                    }
                }

                // Gestion minmax à faire côté python ?
                if (itm_intensity != 0) {
                    // Radius
                    let itm_radius = d.properties[layer.radius.field] || layer.radius.fix;
                    // Orientation
                    let itm_orientation = cls.getOrientation(d, layer)

                    // y, x, intensité, orientation, rayon
                    heatMapData.push([
                        +d.geometry.coordinates[1],
                        +d.geometry.coordinates[0],
                        +(itm_intensity),
                        +(itm_orientation),
                        +(itm_radius)]);
                }
            }
        });
        L.heatLayer(heatMapData, this.heatLayerAttr(layer)).addTo(layer.layer);
    }

    getOrientation(feature, layer) {
        let feat_orientation = feature.properties[layer.orientation.field] || layer.orientation.fix;
        if (layer.orientation.min) {
            feat_orientation = Math.max(layer.orientation.min, feat_orientation)
        }
        if (layer.orientation.max) {
            feat_orientation = Math.min(layer.orientation.max, feat_orientation)
        }
        return feat_orientation
    }

    drawOptions() {
        return {
            draw: {
                rectangle: {
                  shapeOptions: {
                    color: 'violet',
                    fillOpacity: 0.0
                  },
                },
                polyline: false,
                polygon: false,
                marker: false,
                circle: false,
                circlemarker: false,
            },
            edit: false
        }
    }
};

function degrees_to_radians(deg) {
    return deg * Math.PI / 180.0
}