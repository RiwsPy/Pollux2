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


function addPopUp(feature, layer) {
    if (feature.properties) {
        layer.bindPopup(generatePupUpContent(feature) || 'Aucune donnée');
    }
}


function getIcon(feature, icon) {
    return L.icon({
        iconUrl: '../static/img/' + (icon || feature.icon || 'markers/default.png'),
        iconSize: [20, 20],
        });
}


function generatePupUpContent(feature) {
    let content = '';
    // show full data
    for (let [k, v] of Object.entries(feature['properties'])) {
        if (k != 'pk') {
            content += addNewLineInContent(k, v)
        }
    }
    return content
}


function addNewLineInContent(category, content, default_value) {
    content = content || default_value;
    if (content) {
        return '<b>' + category + '</b>: ' + content + '<br>'
    }
    return ''
}


class heatMap {
    constructor(layers, options) {
        this.options = options;
        this.layers = layers;

        if (this.options.zoom.min > this.options.zoom.max) {
            let old_max = this.options.zoom.max;
            this.options.zoom.max = this.options.zoom.min;
            this.options.zoom.min = old_max;
        }
        this.options.zoom.init = Math.min(this.options.zoom.max,
                                    Math.max(this.options.zoom.min, this.options.zoom.init)
                                    )

        this.init()
    }

    init() {
        var controlLayers = {};
        for (let lyr of this.layers) {
            let feature = null;
            if (lyr.style == 'cluster') {
                let radius = function(zoom) {
                    return zoom >= 19? 1: 80;
                };
                feature = new L.markerClusterGroup({maxClusterRadius: radius});
            } else {
                feature = new L.FeatureGroup();
            }
            feature.isActive = lyr.isActive;
            controlLayers[lyr.name] = feature
            lyr.layer = feature
            lyr.data = {};
        }

        this._DB = {};

        this.createMap(controlLayers, false);
        this.loadJson();

        // basic leaflet traduction
        document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
        document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
    }

    createMap(controlLayers, dontCreateMap) {
        let bbox_lat_lng = defaultZoneBound()
        if (this.options.bbox) {
            bbox_lat_lng = L.latLngBounds([
                                [this.options.bbox[1],
                                this.options.bbox[0]],
                                [this.options.bbox[3],
                                this.options.bbox[2]]
                                ]);
        }

        if (!dontCreateMap) {
            let activeLayers = [];
            for (let layer of this.layers) {
                if (layer.isActive) {
                    activeLayers.push(layer.layer)
                }
            }
            this.map = L.map('city_map', {
                    layers: activeLayers,
                    minZoom: this.options.zoom.min,
                    maxZoom: this.options.zoom.max,
                    wheelPxPerZoomLevel: this.options.wheelPxPerZoomLevel
                }).setView(bbox_lat_lng.getCenter(), this.options.zoom.init);
            this.map.owner = this;
        } else {
            this.map.setView(bbox_lat_lng.getCenter(), this.options.zoom.init);

            for (let layer of this.layers) {
                if (layer.isActive) {
                    this.map.addLayer(layer.layer)
                }
            }
        }

        L.control.layers(null, controlLayers).addTo(this.map);

        if (!dontCreateMap) {
            addAttribution(this.map)

            if (this.options.buttons.fullScreen) {
                this.addFullScreenButton()
            }
            if (this.options.draw) {
                this.addDrawControl()
            }
            for (let [id, data] of Object.entries(this.options.buttons)) {
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
        let map = this.map;
        let cls = this;

        map.on('overlayremove ', function(e) {
            for (let layer of cls.layers) {
                if (layer.name == e.name) {
                    layer.isActive = false;
                    break;
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
        if (!this.options.legend) {
            return;
        }

        if (this._legendDiv) {
            this._legendDiv.remove();
        }

        var legend = L.control({ position: "bottomright" });
        let legendBox = L.DomUtil.create("div", "legendBox");
        let legendName = L.DomUtil.create('h4', 'legendName', legendBox);
        legendName.textContent = this.options.legend.name;
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
        if (!this.options.legend || !layer.options.gradient) {
            return;
        }

        if (layer) {
            this.showLegendDetails(layer, maxValue)
        }
    }

    showLegendDetails(layer, maxValue) {
        let i = 0;
        let maxValueInLegend = null;
        maxValue = maxValue || 1.0;
        for (let [legendValue, color] of Object.entries(layer.options.gradient).sort().reverse()) {
            //let lineColor = L.DomUtil.create('i', 'legendButton_' + i, this._legendDiv);
            //lineColor.innerHTML += 'style="background: ' + color + ';"';
            //let lineText = L.DomUtil.create('span', 'legendValue_' + i, this._legendDiv);
            //lineText.textContent = value + '<br>';

            //if (maxValueInLegend == null) {
            //    maxValueInLegend = this.options.legend.max == undefined? legendValue: this.options.legend.max;
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
            if (!(layerdata.db in files_to_load)) {
                files_to_load[layerdata.db] = true;
                this.request(layerdata, fileData);
            }
        };
    }

    request(layerdata) {
        let request = new Request('/api/' + layerdata.db + '?bound=' + this.options.bbox, {
            //method: 'POST',
            method: 'GET',
            //body: JSON.stringify({bbox: this.options.bbox}),
            headers: new Headers({
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
            })
        })
        fetch(request)
        .then((resp) => resp.json())
        .then((data) => {
            this._DB[layerdata.db] = data;
            for (let layer of this.layers) {
                if (layer.db == layerdata.db) {
                    this.createLayer(layer);
                }
            }
        });
    }

    createLayer(layer) {
        if (layer.style == 'heatmap') {
            this.createHeatLayer(this._DB[layer.db], layer)
        } else if (layer.style == 'node' || layer.style == 'cluster') {
            this.createNodeLayer(this._DB[layer.db], layer)
        };
    }

    createNodeLayer(data, layer) {
        let cls = this;
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                let marker = L.marker(latlng, {icon: getIcon(layer),
                                               rotationAngle: cls.getOrientation(feature, layer)});
                addPopUp(feature, marker);
                return marker;
            }
        }).addTo(layer.layer);
    }

    heatLayerAttr(layer) {
        return {
                 max: Math.min(1, Math.max(0, ...Object.keys(layer.gradient))),
                 ...layer,
                }
    }

    createHeatLayer(data, layer) {
        let heatMapData = [];
        let cls = this;
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                let itm_intensity = 0;
                if (layer.value.field) {
                    itm_intensity = d.properties[layer.value.field] || 0;
                } else {
                    itm_intensity = layer.value.fix || 0;
                }
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