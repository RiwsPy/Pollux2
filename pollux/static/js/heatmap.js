/*
 (c) 2014, Vladimir Agafonkin
 simpleheat, a tiny JavaScript library for drawing heatmaps with Canvas
 https://github.com/mourner/simpleheat
 Adapté pour Pollux
*/
!function() {
    "use strict";
    function t(i) {
        return this instanceof t ? (
            this._canvas = i = "string" == typeof i ? document.getElementById(i) : i,
            this._ctx = i.getContext("2d"),
            this._width = i.width,
            this._height = i.height,
            this._max = 1,
            void this.clear()
        ): new t(i)
    }
    t.prototype = {
        defaultRadius: 25,
        defaultGradient: {
            .4: "blue",
            .6: "cyan",
            .7: "lime",
            .8: "yellow",
            1:  "red"
        },
        data: function(t, i) {
            return this._data = t,
            this
        },
        max: function(t) {
            return this._max = t,
            this
        },
        add: function(t) {
            return this._data.push(t),
            this
        },
        clear: function() {
            return this._data = [],
            this
        },
        radius: function(radius, blur, orientation, horizontal_angle) {
            blur = blur === undefined ? 15 : blur;
            orientation = Math.max(0, orientation || 0);
            horizontal_angle = horizontal_angle == undefined ? Math.PI*2 : horizontal_angle;
            var a = this._circle = document.createElement("canvas"),
                s = a.getContext("2d"),
                e = this._r = Math.max(1, radius);

            if (blur > radius) {
                console.log(blur + ' ' + radius)
            }

            // bug horizontal_angle car le point d'origine est fixe
            return a.width = 2*e,
                    a.height = 2*e,
                    s.shadowOffsetX = s.shadowOffsetY = 800,
                    s.shadowBlur = blur,
                    s.shadowColor = "black",
                    s.beginPath(),
                    // (x, y, rayon, angle de départ, angle de fin, sensHoraire)
                    s.arc(e-800, e-800, Math.max(0, radius - blur), orientation, orientation + horizontal_angle, !0),
                    s.closePath(), // ferme la forme
                    s.fill(), // rempli, sinon stroke
                    this
        },
        gradient: function(t) {
            var i = document.createElement("canvas"),
                a = i.getContext("2d"),
                s = a.createLinearGradient(0, 0, 0, 256);
            i.width = 1,
            i.height = 256;
            for (var e in t) {
                s.addColorStop(e, t[e])
            }
            return a.fillStyle = s,
                    a.fillRect(0, 0, 1, 256),
                    this._grad = a.getImageData(0, 0, 1, 256).data,
                    this
        },
        draw: function(opacity) {
            this._grad || this.gradient(this.defaultGradient);
            var i = this._ctx;
            i.clearRect(0, 0, this._width, this._height);
            for (var a,
                     s = 0,
                     e = this._data.length;
                 e > s ; s++) {
                a = this._data[s];
                this.radius(a.radius, a.blur, a.orientation/360*Math.PI*2, a.horizontal_angle/360*Math.PI*2);
                i.globalAlpha = Math.max(a.intensity / this._max, opacity || .05);
                i.drawImage(this._circle, a.x - this._r, a.y - this._r);
            };

            var n = i.getImageData(0, 0, this._width, this._height);
            return this._colorize(n.data, this._grad),
                    i.putImageData(n, 0, 0),
                    this
        },
        _colorize: function(t, i) {
            for (var a,
                     s = 3,
                     e = t.length;
                 e > s ; s += 4) {
                a = 4 * t[s],
                a && (t[s-3] = i[a],
                      t[s-2] = i[a+1],
                      t[s-1] = i[a+2])
            }
        }
    },
    window.simpleheat = t
}(),/*
 (c) 2014, Vladimir Agafonkin
 Leaflet.heat, a tiny and fast heatmap plugin for Leaflet.
 https://github.com/Leaflet/Leaflet.heat
*/


L.HeatLayer = (L.Layer ? L.Layer : L.Class).extend({
    initialize: function (latlngs, options) {
        this._latlngs = latlngs;
        L.setOptions(this, options);
    },

    setLatLngs: function (latlngs) {
        this._latlngs = latlngs;
        return this.redraw();
    },

    addLatLng: function (latlng) {
        this._latlngs.push(latlng);
        return this.redraw();
    },

    setOptions: function (options) {
        L.setOptions(this, options);
        if (this._heat) {
            this._updateOptions();
        }
        return this.redraw();
    },

    redraw: function () {
        if (this._heat && !this._frame && this._map && !this._map._animating) {
            this._frame = L.Util.requestAnimFrame(this._redraw, this);
        }
        return this;
    },

    onAdd: function (map) {
        this._map = map;

        if (!this._canvas) {
            this._initCanvas();
        }

        if (this.options.pane) {
            this.getPane().appendChild(this._canvas);
        } else {
            map._panes.overlayPane.appendChild(this._canvas);
        }

        map.on('moveend', this._reset, this);

        if (map.options.zoomAnimation && L.Browser.any3d) {
            map.on('zoomanim', this._animateZoom, this);
        }

        this._reset();
    },

    onRemove: function (map) {
        if (this.options.pane) {
            this.getPane().removeChild(this._canvas);
        } else {
            map.getPanes().overlayPane.removeChild(this._canvas);
        }

        map.off('moveend', this._reset, this);

        if (map.options.zoomAnimation) {
            map.off('zoomanim', this._animateZoom, this);
        }
    },

    addTo: function (map) {
        map.addLayer(this);
        return this;
    },

    getRadius: function (radiusValue) {
        //radiusValue = this.options.radius.fix || radiusValue;
        if (this.options.radius.unit === 'auto') {
            radiusValue = Math.min(radiusValue / metresPerPixel(this._map), radiusValue*2);
        // réalisme ++ mais parfois non exploitable en zoomant
        } else if (this.options.radius.unit === 'meter') {
            radiusValue /= metresPerPixel(this._map);
        }

        radiusValue = Math.max(0, radiusValue + this.options.radius.add)
        if (this.options.radius.max != undefined) {
            radiusValue = Math.min(this.options.radius.max, radiusValue)
        }
        if (this.options.radius.min != undefined) {
            radiusValue = Math.max(this.options.radius.min, radiusValue)
        }
        return radiusValue
    },

    getBlur: function (blurValue, radius) {
        if (this.options.blur.unit == '%' && this.options.blur.fix) {
            blurValue = radius * this.options.blur.fix / 100;
        } else if (this.options.radius.unit === 'auto') {
            blurValue = Math.min(blurValue / metresPerPixel(this._map), radius/2, blurValue);
        } else if (this.options.radius.unit === 'meter') {
            blurValue /= metresPerPixel(this._map);
        }
        if (this.options.blur.min != undefined) {
            blurValue = Math.max(blurValue, this.options.blur.min);
        }
        if (this.options.blur.max != undefined) {
            blurValue = Math.min(blurValue, this.options.blur.max);
        }
        //blurValue = Math.min(blurValue, radius);

        return blurValue;
    },

    _initCanvas: function () {
        var canvas = this._canvas = L.DomUtil.create('canvas', 'leaflet-heatmap-layer leaflet-layer');

        var originProp = L.DomUtil.testProp(['transformOrigin', 'WebkitTransformOrigin', 'msTransformOrigin']);
        canvas.style[originProp] = '50% 50%';

        var size = this._map.getSize();
        canvas.width  = size.x;
        canvas.height = size.y;

        var animated = this._map.options.zoomAnimation && L.Browser.any3d;
        L.DomUtil.addClass(canvas, 'leaflet-zoom-' + (animated ? 'animated' : 'hide'));

        this._heat = simpleheat(canvas);
        this._updateOptions();
    },

    _updateOptions: function () {
        if (this.options.gradient) {
            this._heat.gradient(this.options.gradient);
        }
    },

    _reset: function () {
        var topLeft = this._map.containerPointToLayerPoint([0, 0]);
        L.DomUtil.setPosition(this._canvas, topLeft);

        var size = this._map.getSize();

        if (this._heat._width !== size.x) {
            this._canvas.width = this._heat._width = size.x;
        }
        if (this._heat._height !== size.y) {
            this._canvas.height = this._heat._height = size.y;
        }

        this._redraw();
    },

    _redraw: function () {
        if (!this._map) {
            return;
        }

        var data = [],
            r = 1, //this._heat._r/8,
            size = this._map.getSize(),
            bounds = new L.Bounds(
                L.point([-r, -r]),
                size.add([r, r])),
            cellSize = r / 2,
            grid = [],
            panePos = this._map._getMapPanePos(),
            offsetX = panePos.x % cellSize,
            offsetY = panePos.y % cellSize,
            i, len, p, cell, x, y, j, len2;

        this._max = 1;

        // console.time('process');
        for (i = 0, len = this._latlngs.length; i < len; i++) {
            p = this._map.latLngToContainerPoint([this._latlngs[i].lat,
                                                  this._latlngs[i].lng,
                                                  this._latlngs[i].intensity]);
            //p = this._map.latLngToContainerPoint(this._latlngs[i]); // pixel correspondant aux coordonnées
            x = Math.floor((p.x - offsetX) / cellSize) + 2;
            y = Math.floor((p.y - offsetY) / cellSize) + 2;

            var alt =
                this._latlngs[i].alt !== undefined ? this._latlngs[i].alt :
                this._latlngs[i].intensity !== undefined ? this._latlngs[i].intensity : 0;

            grid[y] = grid[y] || [];
            cell = grid[y][x];

            // position moyenne pondérée par le niveau d'intensité
            if (!cell) {
                cell = grid[y][x] = {x: p.x,
                                     y: p.y,
                                     intensity: alt,
                                     orientation: this._latlngs[i].orientation,
                                     horizontal_angle: this._latlngs[i].horizontal_angle,
                                     radius: this.getRadius(this._latlngs[i].radius)};
                cell.p = p;
            } else {
                cell.x = (cell.x * cell.intensity + p.x * alt) / (cell.intensity + alt); // x
                cell.y = (cell.y * cell.intensity + p.y * alt) / (cell.intensity + alt); // y
                cell.intensity += alt; // cumulated intensity value
                cell.horizontal_angle = Math.max(cell.horizontal_angle, this._latlngs[i].horizontal_angle);
                if (Math.abs(cell.orientation - this._latlngs[i].orientation) > 170 &&
                            Math.abs(cell.orientation - this._latlngs[i].orientation) < 190) {
                    cell.horizontal_angle = 360;
                } else {
                    cell.orientation = (cell.orientation + this._latlngs[i].orientation)/2;
                }
                cell.radius = Math.max(cell.radius, this.getRadius(this._latlngs[i].radius))
            }

            // Set the max for the current zoom level
            this._max = Math.max(this._max, cell.intensity)
        }

        this.updateMax(grid)
        this._heat.max(this._max);

        for (i = 0, len = grid.length; i < len; i++) {
            if (grid[i]) {
                for (j = 0, len2 = grid[i].length; j < len2; j++) {
                    cell = grid[i][j];
                    if (cell && cell.intensity > 0 && bounds.contains(cell.p)) {
                        data.push({
                            x: Math.round(cell.x),
                            y: Math.round(cell.y),
                            intensity: Math.min(cell.intensity, this._max),
                            radius: cell.radius,
                            orientation: cell.orientation,
                            horizontal_angle: cell.horizontal_angle,
                            blur: this.getBlur(this.options.blur.fix, cell.radius)
                        })
                    }
                }
            }
        }
        // console.timeEnd('process');

        // console.time('draw ' + data.length);

        this._heat.data(data).draw(this.options.minOpacity);
        // console.timeEnd('draw ' + data.length);

        this._frame = null;

        // Legend update
        this._map.owner.addLegend(this, this._max)

    },

    _animateZoom: function (e) {
        var scale = this._map.getZoomScale(e.zoom),
            offset = this._map._getCenterOffset(e.center)._multiplyBy(-scale).subtract(this._map._getMapPanePos());

        if (L.DomUtil.setTransform) {
            L.DomUtil.setTransform(this._canvas, offset, scale);

        } else {
            this._canvas.style[L.DomUtil.TRANSFORM] = L.DomUtil.getTranslateString(offset) + ' scale(' + scale + ')';
        }
    },

    updateMax(grid) {
        if (this.options.maxValue.method === 'part%') {
            let maxValue = Math.max(0, this.options.maxValue.fix);
            values = []
            for (x in grid) {
                for (y in grid[x]) {
                    if (grid[x][y].intensity) {
                        values.push(Math.abs(grid[x][y].intensity))
                    }
                }
            }
            values = values.sort(function(a, b){return a - b});
            this._max = values[Math.ceil(values.length*maxValue/100)];
        } else if (this.options.maxValue.method == 'zoom_depend') {
            // Contrôle de la valeur max en fonction du Zoom
            let getZoom = this._map.getZoom();
            this._max = this.options.maxValue.gradient[getZoom] ||
                        this.options.maxValue.gradient[Math.round(getZoom)] ||
                        1;
        } else if (this.options.maxValue.method == 'fix') {
            this._max = this.options.maxValue.fix;
        } else if (this.options.maxValue.method === '%') {
            let maxValue = Math.max(0, Math.min(1, this.options.maxValue.fix));
            this._max *= maxValue;
        }
    }
});

L.heatLayer = function (latlngs, options) {
    return new L.HeatLayer(latlngs, options);
};

function metresPerPixel(map) {
    // 40075016.686 : circonférence terrestre (mètre)
    return 40075016.686 * Math.abs(Math.cos(map.getCenter().lat * Math.PI/180)) / Math.pow(2, map.getZoom()+8);
}


const clamp = (num, min, max) => num < min ? min : num > max ? max : num;

function tmpKelvin(tmpKelvin) {
	// All calculations require tmpKelvin \ 100, so only do the conversion once
	tmpKelvin = clamp(tmpKelvin, 1000, 40000) / 100;

	// Note: The R-squared values for each approximation follow each calculation
	return {
		r: tmpKelvin <= 66 ? 255 :
			clamp(329.698727446 * (Math.pow(tmpKelvin - 60, -0.1332047592)), 0, 255),  // .988

		g: tmpKelvin <= 66 ?
			clamp(99.4708025861 * Math.log(tmpKelvin) - 161.1195681661, 0, 255) :      // .996
			clamp(288.1221695283 * (Math.pow(tmpKelvin - 60, -0.0755148492)), 0, 255), // .987

		b: tmpKelvin >= 66 ? 255 :
			tmpKelvin <= 19 ? 0 :
			clamp(138.5177312231 * Math.log(tmpKelvin - 10) - 305.0447927307, 0, 255)  // .998
	};
};