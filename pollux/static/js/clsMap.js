function defaultZonePos() {
    //return [[45.187501, 5.704696], [45.198848, 5.725703]];
    return [[45.15008475740563, 5.664997100830078], [45.221347171208436, 5.766019821166993]]
}

function zonePos(bbox) {
    return L.latLngBounds([
                           [bbox[1],
                            bbox[0]],
                           [bbox[3],
                            bbox[2]]
                        ])
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


function addAttribution(map, options) {
    let tileLayer = L.tileLayer(
        options.url,
        {
            maxZoom: options.maxZoom,
            attribution: options.attribution
        }).addTo(map);
        //'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
        //'https://tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey=XX', {
        //'https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
        //'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        //attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
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
    constructor(layers, options, ID) {
        this.ID = ID;
        this.options = options;
        this.layers = layers;
        this.options.filters = this.options.filters || {};

        /*
        for (let layer of this.layers) {
            layer['filters'] = JSON.stringify(layer['filters']);
        }
        */

        if (this.options.zoom.min > this.options.zoom.max) {
            let old_max = this.options.zoom.max;
            this.options.zoom.max = this.options.zoom.min;
            this.options.zoom.min = old_max;
        }
        this.options.zoom.max = Math.min(this.options.zoom.max, this.options.tile_layer.maxZoom);
        this.options.zoom.init = Math.min(this.options.zoom.max,
                                    Math.max(this.options.zoom.min, this.options.zoom.init)
                                    );

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
        let bbox_lat_lng = undefined;
        if (this.url_get_paramaters('filters')) {
            // Position dans l'URL
            bbox_lat_lng = JSON.parse(this.url_get_paramaters('filters'))['position__within'];
        }
        if (!bbox_lat_lng) {
            // Position du filtre n°1
            bbox_lat_lng = this.layers[0].filters.position__within;

            // Position du premier filtre actif
            for (let layer of this.layers) {
                if (layer.isActive) {
                    bbox_lat_lng = layer.filters['position__within'];
                    break;
                }
            }
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
                    zoomDelta: this.options.zoom.button,  // granularité du zoom (bouton)
                    zoomSnap: 0.1,  // modulo minimum
                    wheelPxPerZoomLevel: 75/this.options.zoom.scroll  // granularité du zoom (scroll)
                }).setView(zonePos(bbox_lat_lng).getCenter(), this.options.zoom.init);
            this.map.owner = this;
        } else {
            this.map.setView(zonePos(bbox_lat_lng).getCenter(), this.options.zoom.init);

            for (let layer of this.layers) {
                if (layer.isActive) {
                    this.map.addLayer(layer.layer)
                }
            }
        }

        L.control.layers(null, controlLayers).addTo(this.map);

        if (!dontCreateMap) {
            addAttribution(this.map, this.options.tile_layer)

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
        this.options.filters = JSON.parse(this.url_get_paramaters('filters')) || {};
        this.options.filters.position__within = bound;

        let url = '?zoom=' + this.map.getZoom() +
            '&layers=' +
            (activeNbLayers.join('/') || -1);
            /*
            '&bound=' +
            bound[0].toFixed(6) + '/' +
            bound[1].toFixed(6) + '/' +
            bound[2].toFixed(6) + '/' +
            bound[3].toFixed(6);
            */
        url += '&filters=' + JSON.stringify(this.options.filters)

        window.location.href = url

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

    async loadJson() {
        let layer_id = 0;
        let layer_in_progress = {};
        for await (let layerdata of this.layers) {
            //if (!layer_in_progress[layerdata.db] ||
            //        !layer_in_progress[layerdata.db][layerdata.filters]) {
                layer_in_progress[layerdata.db] = layer_in_progress[layerdata.db] || {};
                layer_in_progress[layerdata.db][layerdata.filters] = true;
                this.request(layerdata, layer_id);
            //}
            layer_id += 1;
        };
    }

    url_get_paramaters(param) {
        let str_url = new URL(window.location.href);
        return str_url.searchParams.get(param)
    }

    request(layerdata, layer_id) {
       this._DB[layerdata.db] = this._DB[layerdata.db] || {};

        // récupérer tous les attributs de l'URL ??
        let url = '/api/' + layerdata.db //+ '?bound=' + this.options.bbox
        url += '?map_id=' + this.ID || -1
        url += '&layer_id=' + layer_id || -1
        let filters = this.url_get_paramaters('filters')
        if (filters) {
            url += '&filters=' + filters
        }

        let request = new Request(url, {
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
           this._DB[layerdata.db][JSON.stringify(layerdata.filters)] = data;
           for (let layer of this.layers) {
                if (layer.db == layerdata.db &&
                        JSON.stringify(layer.filters) == JSON.stringify(layerdata.filters)) {
                    this.createLayer(layer);
                }
            }
        });
    }

    createLayer(layer) {
        let data = this._DB[layer.db][JSON.stringify(layer.filters)];
        if (layer.type == 'heatmap') {
            this.createHeatLayer(data, layer)
        } else if (layer.type == 'node' || layer.type == 'cluster') {
            this.createNodeLayer(data, layer)
        };
    }

    createNodeLayer(data, layer) {
        let cls = this;
        L.geoJSON(data, {
            style: layer.style,
            onEachFeature: function(feature, layer) {
                addPopUp(feature, layer);
            },
            pointToLayer: function(feature, latlng) {
                let marker = L.marker(latlng, {icon: getIcon(layer),
                                               rotationAngle: cls.getOrientation(feature, layer)});
                //addPopUp(feature, marker);
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
                    heatMapData.push({
                        lng: d.geometry.coordinates[0],
                        lat: d.geometry.coordinates[1],
                        intensity: itm_intensity,
                        orientation: cls.getOrientation(d, layer),
                        radius: d.properties[layer.radius.field] || layer.radius.fix,
                        horizontal_angle: cls.getHorizontalAngle(d, layer),
                    })
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

    getHorizontalAngle(feature, layer) {
        let feat_hangle = feature.properties[layer.horizontal_angle.field] || layer.horizontal_angle.fix;
        if (layer.horizontal_angle.min) {
            feat_hangle = Math.max(layer.horizontal_angle.min, feat_hangle)
        }
        if (layer.horizontal_angle.max) {
            feat_hangle = Math.min(layer.horizontal_angle.max, feat_hangle)
        }
        return feat_hangle
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