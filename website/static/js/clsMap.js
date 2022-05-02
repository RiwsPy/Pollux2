function defaultZonePos() {
    //return [[45.187501, 5.704696], [45.198848, 5.725703]];
    return [[45.15008475740563, 5.664997100830078], [45.221347171208436, 5.766019821166993]]
}

function defaultZoneBound() {
    return L.latLngBounds(defaultZonePos());
}


function addAttribution(map) {
    // choix à ajouter
    /*
    if (mapName == 'Impact') {
        let tileLayer = L.tileLayer('//{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png', {
            maxZoom: 20,
            attribution: 'donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
            }).addTo(map);
    } else {*/
    let tileLayer = L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png', {
        maxZoom: 20,
        attribution: '<a href="https://green-pollux.herokuapp.com">Pollux</a>, &copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
        }).addTo(map);
    //}
}


function addPopUp(feature, layer, categoryName, invertIntensity) {
    if (feature.properties) {
        layer.bindPopup(generatePupUpContent(feature, categoryName, invertIntensity) || 'Aucune donnée');
    }
}

function getIcon(feature, icon) {
    return L.icon({
        iconUrl: '../static/img/' + (icon || feature.icon || 'markers/default.png'),
        iconSize: [20, 20],
        });
}

function generateClipsContent(obj, category_name) {
    let ret = {type: category_name}
    if (category_name === 'Tree') {
        ret.genre = obj.properties.GENRE_BOTA
        ret.species = obj.properties.ESPECE
    } else if (category_name == 'Shop') {
        ret.openingHours = obj.properties.opening_hours
        ret.name = obj.properties.name
    } else if (category_name == 'Animal') {
        ret.species = obj.properties.NomCite
        ret.speciesScient = obj.properties.NomScientifiqueRef
        ret.sensible = obj.properties.Sensible
    } else if (category_name == 'BusLine') {
        ret.openingHours = 'Mo-Su 05:00-24:00'
        ret.name = obj.properties.LIBELLE
        ret.line_number = obj.properties.NUMERO
    } else if (category_name == 'PublicTransportStop') {
        ret.openingHours = 'Mo-Su 05:00-24:00'
        ret.name = obj.properties.name
    }
    return ret
}


function generatePupUpContent(feature, categoryName, invertIntensity) {
    let content = '';
    if (categoryName == 'Park') {
        content += addNewLineInContent('Nom', feature.properties.name)
    } else if (categoryName == 'Tree') {
        content += addNewLineInContent('Arbre', feature.properties.taxon)
        content += addNewLineInContent('Année de plantation', feature.properties.planted_date, 'Inconnue')
    } else if (categoryName == 'BusLine') {
        content += addNewLineInContent('Ligne de bus', feature.properties.numero + ' ' + feature.properties.name)
    } else if (categoryName == 'Animal') {
        content += addNewLineInContent('Taxon', feature.properties.NomVernaculaire)
    } else if (categoryName == 'Lamp') {
        content += addNewLineInContent('Luminaire n°', feature.properties.code)
        content += addNewLineInContent('Température (K)', feature.properties.colour)
        content += addNewLineInContent('Rendu couleur (%)', feature.properties.irc)
        content += addNewLineInContent('Réduction nocturne (%)', feature.properties.lowering_night)
        content += addNewLineInContent('Hauteur (m)', feature.properties.height)
    } else if (categoryName == 'Shop') {
        content += addNewLineInContent('Nom', feature.properties.name)
        content += addNewLineInContent("Horaires d'ouvertures", feature.properties.opening_hours, 'Inconnues')
    }
    /*
    // show full data
    for (let [k, v] of Object.entries(feature['properties'])) {
        content += addNewLineInContent(k, v)
    }
    */
    if (feature['properties']['_pollux_values']) {
        for (let [k, v] of Object.entries(feature['properties']['_pollux_values'])) {
            // TODO: les valeurs ne sont pas nécessairement maxées à 1, de quelle valeur faut-il faire la différence ?
            v = (invertIntensity  && k != 'Différence') ? 1- Math.min(v, 1): v,
            content += addNewLineInContent('Calque ' + k, v.toFixed(2), "0")
        }
    }
    return content //+ '<br>+ recommandations connues'
}


function addNewLineInContent(category, content, default_value) {
    content = content || default_value;
    if (content) {
        return '<b>' + category + '</b> : ' + content + '<br>'
    }
    return ''
}


function createRectangle(bound, color, fillColor, fillOpacity) {
    return L.rectangle(bound, {
        color: color || 'green',
        fillColor: fillColor || '#3c0',
        fillOpacity: fillOpacity || 0.1,
    })
}


function createCircle(ePosition, color, fillColor, fillOpacity, radius) {
    return L.circle(ePosition, {
        color: color || 'red',
        fillColor: fillColor || '#f03',
        fillOpacity: fillOpacity || 0.5,
        radius: radius || 10,
    })
}


function addDescButton(map) {
    let url = new URL(window.location.href)
    let url_split = url.pathname.split('/')
    let map_id = url_split[2]
    let htmlValue = '<a id="mapButton" href="/map_desc/' + map_id + '" title="Ouvrir la description" target="_blank"><i style="width: 17px;" class="fa fa-book fa-lg"></i></a>'
    addButton(map, htmlValue)
}


function addHomeButton(map) {
    addButton(map,
              '<a id="mapButton" href="/" title="Retour à l\'accueil"><i style="width: 17px;" class="fas fa-door-open"></i></a>'
             )
}


function addButton(map, htmlValue) {
    let homeButton = L.control({ position: "topleft" });
    homeButton.onAdd = function(map) {
        let div = L.DomUtil.create("div");
        div.innerHTML += htmlValue
        return div;
    };
    homeButton.addTo(map);
}

function reverse_polygon_pos(coordinates) {
    let ret = [[]];
    for (lines of coordinates) {
        for (position of lines) {
            ret[0].push(position.slice().reverse())
        }
    }
    return ret
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
            maxZoom: 20,
            radius: 30,
            blur: 0,
            legend: true,
            fullScreenButton: true,
            descButton: true,
            homeButton: true,
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
                maxZoom: 20,
                radius: 30,
                blur: 15,
                legend: {name: 'Légende'},
                draw: true,
                fullScreenButton: true,
                descButton: true,
                homeButton: true,
                gradient: defaultLegendColor,
            },
            ...options
        };

        let params = window.location.href.split('/')
        this.invertIntensity = params[params.length - 1][0] == '-'

        for (let lyr of layers) {
            if (lyr.layerType == 'cluster') {
                let radius = function(zoom) {
                    if (zoom >= 19) {
                        return 1;
                    } else {
                        return 80;
                    }
                };
                lyr.layer = new L.markerClusterGroup({maxClusterRadius: radius});
            } else {
                lyr.layer = new L.FeatureGroup();
            }
            lyr.data = {};
        }

        this.layers = layers;
        this._DB = {};

        let controlLayers = this.createLayers();

        this.createMap(controlLayers);
        this.loadJson();

        // basic leaflet traduction
        document.getElementsByClassName('leaflet-control-zoom-in')[0].title = 'Zoom avant';
        document.getElementsByClassName('leaflet-control-zoom-out')[0].title = 'Zoom arrière';
    }

    createLayers() {
        //let baseClickableZone = createRectangle(defaultZoneBound(), 'yellow'); // rectangle représentant la zone de test
        this._baseLayer = new L.FeatureGroup(); // [baseClickableZone]); // calque contenant le rectangle

        var controlLayers = {
            //"Zone Test": this._baseLayer,
        };
        if (this._options.draw) { // calque dessin
            this._drawLayer = new L.FeatureGroup();
            controlLayers['Mon Calque'] = this._drawLayer;
        }
        for (let fileData of this.layers) {
            controlLayers[fileData.layerName] = fileData.layer
        };
        return controlLayers
    }

    createMap(controlLayers) {
        this.map = L.map('city_map', {
                layers: [this._baseLayer, this._drawLayer || this.layers[0].layer],
                minZoom: 14,
                wheelPxPerZoomLevel: 120 // 1 niveau de zoom par scroll
            }).setView(defaultZoneBound().getCenter(), 15);

        L.control.layers(null, controlLayers).addTo(this.map);
        addAttribution(this.map)

        if (this._options.fullScreenButton) {
            this.addFullScreenButton()
        }
        if (this._options.draw) {
            this.addDrawControl()
        }
        if (this._options.legend) {
            this.addLegend()
        }
        if (this._options.descButton) {
            addDescButton(this.map)
        }
        if (this._options.homeButton) {
            addHomeButton(this.map)
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
        this.map.addControl(new L.Control.Draw(this.drawOptions()));
    }

    addLegend(position) {
        if (this._mapLegend) {
            this.updateLegend(this.layers)
        } else {
            var legend = L.control({ position: position || "bottomright" });
            this._mapLegend = legend;
            this._legendDiv = L.DomUtil.create("div", "legend");
            this._legendDiv.innerHTML += "<h4>" + this._options.legend.name + "</h4>"
            let ret = this._legendDiv
            this.updateLegend()
            legend.onAdd = function(map) {
                return ret
            };
            legend.addTo(this.map);
        }
    }

    updateLegend() {
        if (!this._options.legend) {
            return;
        }

        let i = 0;
        for (let [value, color] of Object.entries(this._options.gradient).sort().reverse()) {
            this._legendDiv.innerHTML += '<i id="legendButton_' + i + '" style="background: ' + color + '"></i>'
            this._legendDiv.innerHTML += '<span>' + ' >= ' + '<span id="legendValue_' + i + '">' + value + '</span>' + '</span><br>'
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
        let request = new Request('/api/' + layerdata.filename, {
            method: 'GET',
            headers: new Headers(),
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
        if (layer.layerType == 'heatmap_intensity') {
            this.createHeatLayer(this._DB[layer.filename], layer)
        }
        else if (layer.layerType == 'heatmap') {
            this.createHeatLayer(this._DB[layer.filename], layer, 1)
        } else if (layer.layerType == 'node') {
            this.createNodeLayer(this._DB[layer.filename], layer)
        } else if (layer.layerType == 'cluster') {
            this.createClusterLayer(this._DB[layer.filename], layer)
        };
    }

    createNodeLayer(data, layer) {
        let layerName1 = this.layers[0].layerName
        let invertIntensity = this.invertIntensity;
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                let marker = L.marker(latlng, {icon: getIcon(layer)});
                addPopUp(feature, marker, layer.entityType, invertIntensity);
                return marker;
            }
        }).addTo(layer.layer);
    }

    createClusterLayer(data, layer) {
        let layerName1 = this.layers[0].layerName
        let invertIntensity = this.invertIntensity;
        L.geoJSON(data, {
            pointToLayer: function(feature, latlng) {
                let marker = L.marker(latlng, {icon: getIcon(layer)});
                addPopUp(feature, marker, layer.entityType, invertIntensity);
                return marker;
            }
        }).addTo(layer.layer);
    }

    heatLayerAttr() {
        return {
                 maxZoom: this._options.maxZoom,
                 radius: this._options.radius,
                 blur: this._options.blur,
                 gradient: this._options.gradient,
                 max: Math.min(1, Math.max(0, ...Object.keys(this._options.gradient))),
                }
    }

    createHeatLayer(data, layer, default_intensity) {
        let heatMapData = [];
        let invertIntensity = this.invertIntensity
        data.features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                let intensity = Math.min(1,
                                    d.properties['_pollux_values'][layer.valueName] ||
                                    d.properties['_pollux_values'][layer.layerName])
                intensity = invertIntensity && layer.layerName != 'Différence' ? 1- (intensity || 0) : intensity
                heatMapData.push([
                    +d.geometry.coordinates[1],
                    +d.geometry.coordinates[0],
                    // TODO: change this bullshit
                    //+Math.max(...d.geometry.coordinates),
                    //+Math.min(...d.geometry.coordinates),
                    //
                    +(default_intensity || intensity)]);
            }
        });
        L.heatLayer(heatMapData, this.heatLayerAttr()).addTo(layer.layer);
    }

    drawOptions() {
        return {
            draw: {
                rectangle: {
                  shapeOptions: {
                    color: '#97009c'
                  },
                  //repeatMode: true,
                },
                circle: {
                  shapeOptions: {
                    color: '#b7000c'
                  },
                  //repeatMode: true,
                },
                polygon: {
                  shapeOptions: {
                    color: '#07b90c'
                  },
                  //repeatMode: true,
                },
                circlemarker: {
                  //repeatMode: true,
                },

                polyline: false,
                polygon: false,
                marker: false,
            },
            edit: {
                featureGroup: this._drawLayer,
                remove: true
            }
        }
    }
};




class recommendationMap extends heatMap {
    addDrawControl() {
        this.map.addControl(new L.Control.Draw(this.drawOptions()));
        this.addTemporaryCircleOnClick()
    }

    addTemporaryCircleOnClick() {
        // temporary circle with simple click
        let editableLayer = this._drawLayer;
        let map = this.map;
        let tempForm = this._tempForm;
        let blockTempForm = this._blockTempForm;
        let cls = this;

        this.map.on('click', function(e) {
            if (!cls._blockTempForm & defaultZoneBound().contains(e.latlng)) {
                if (cls._tempForm !== null) {
                    cls._drawLayer.removeLayer(cls._tempForm);
                    //map.removeLayer(tempForm);
                }
                cls._tempForm = createCircle(e.latlng, {radius:10}).addTo(cls.map);
                cls.createTooltipContent(cls._tempForm);
                cls._drawLayer.addLayer(cls._tempForm);
            }
        });

        // lock default click if a new form is drawing
        this.map.on('draw:drawstart', function(e) {
            cls.lockTempForm();
        })
        this.map.on('draw:deletestart', function(e) {
            cls.lockTempForm();
        })

        // unlock
        this.map.on('draw:drawstop', function(e) {
            cls.unlockTempForm();
        })
        this.map.on('draw:deletestop', function(e) {
            cls.unlockTempForm();
        })

        // create form
        map.on('draw:created', function(e) {
            var layer = e.layer;
            cls.createTooltipContent(layer);
            editableLayer.addLayer(layer);
        });


        // tooltip update
        map.on('draw:edited', function(e) {
            for (var layer of Object.values(e.layers._layers)) {
                cls.createTooltipContent(layer);
            }
        });
    }

    lockTempForm() {
        this._blockTempForm = true;
    }

    unlockTempForm() {
        this._blockTempForm = false;
    }

    createTooltipContent(form) {
        let tooltipContent = '';
        let hasArea = 0.0;
        let latLng = {lat: 0.0, lng: 0.0};
        let influencingElements = [];

        var requestClips = {
            schedule: '2023-02-01 08:00',
        }

        if (form instanceof L.CircleMarker) { // include Circle
            for (let layer of this.layers) {
                let nbObj_clipsData = this.nbObjInRange(layer, form.getLatLng(), form.getRadius());
                influencingElements.push(...nbObj_clipsData[1])
                tooltipContent += '<b>' + layer.layerName + '</b>:' + nbObj_clipsData[0] + '<br/>';
            }
            hasArea = form.getRadius()*form.getRadius()*3.141592654;
            latLng = form.getLatLng();
        } else if (form instanceof L.Polygon) { // include Rectangle
            for (let layer of this.layers) {
                let nbObj_clipsData = this.nbObjInBound(layer, form.getBounds());
                influencingElements.push(...nbObj_clipsData[1])
                tooltipContent += '<b>' + layer.layerName + '</b>:' + nbObj_clipsData[0] + '<br/>';
            }
            hasArea = L.GeometryUtil.geodesicArea(form.getLatLngs()[0]);
            latLng = form.getBounds().getCenter();
        }

        requestClips.hasArea = hasArea;
        requestClips.latLng = latLng;
        requestClips.InfluencingElements = influencingElements;

        if (form != null) {
            form.bindTooltip(tooltipContent)
        }

        clipsRequest(requestClips)
    }

    nbObjInRange(layer, ePosition, radius) {
        let nbObj = 0;
        let requestClips = [];
        let cls = this;
        this._DB[layer.filename].features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                if (cls.map.distance(ePosition, d.geometry.coordinates.slice().reverse()) <= radius) {
                    nbObj += 1;
                    requestClips.push(generateClipsContent(d, layer.entityType))
                }
            } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
                if (d.geometry.type == 'Polygon' &
                    L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).contains(ePosition)) {
                        nbObj += 1
                        requestClips.push(generateClipsContent(d, layer.entityType))
                } else {
                    for (lines of d.geometry.coordinates) {
                        for (position of lines) {
                            if (ePosition.distanceTo(position.slice().reverse()) <= radius) {
                                nbObj += 1
                                requestClips.push(generateClipsContent(d, layer.entityType))
                                break
                                break
                            }
                        }
                    }
                }
            }
        });
        return [nbObj, requestClips];
    }

    nbObjInBound(layer, bound) {
        let nbObj = 0;
        let requestClips = [];
        this._DB[layer.filename].features.forEach(function(d) {
            if (d.geometry.type == 'Point') {
                if (bound.contains(d.geometry.coordinates.slice().reverse())) {
                    nbObj += 1;
                    requestClips.push(generateClipsContent(d, layer.entityType))
                }
            } else if (d.geometry.type == 'MultiLineString' || d.geometry.type == 'Polygon') {
                if (d.geometry.type == 'Polygon' &
                    L.latLngBounds(reverse_polygon_pos(d.geometry.coordinates)).intersects(bound)) {
                        nbObj += 1;
                        requestClips.push(generateClipsContent(d, layer.entityType))
                } else {
                    for (lines of d.geometry.coordinates) {
                        for (position of lines) {
                            if (bound.contains(position.slice().reverse())) {
                                nbObj += 1;
                                requestClips.push(generateClipsContent(d, layer.entityType))
                                break
                                break
                            }
                        }
                    }
                }
            }
        });
        return [nbObj, requestClips];
    }
}

function clipsRequest(requestClips) {
    let request = new Request('/clips/', {
        method: 'POST',
        headers: new Headers(),
        body: JSON.stringify(requestClips),
        })

    fetch(request)
    .then((resp) => resp.json())
    .then((data) => {
        let recommendationContent = document.getElementById("clips_recommendations_content");
        recommendationContent.innerHTML = data.recommendation;
    });
}