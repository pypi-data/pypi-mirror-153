/*global mapboxgl satellite */

$(document).ready(function() {
    'use strict';

    var sin = Math.sin;
    var cos = Math.cos;
    var fabs = Math.abs;
    var acos = Math.acos;
    var asin = Math.asin;

    var pi = Math.pi;
    var earthRadius = 6.378135E3;  /* Earth radius km */
    var de2ra = 1.74532925E-2;  /* Degrees to Radians */
    var pio2     =1.5707963267949;  /* Pi/2 */

    var tle1 = $('div#map').data('tle1');
    var tle2 = $('div#map').data('tle2');
    var mapboxtoken = $('div#map').data('mapboxtoken');

    mapboxgl.accessToken = mapboxtoken;

    /* Returns angle in radians from arg id degrees */
    function radians(arg) {
        return (arg * de2ra);
    }

    /* Returns angle in degrees from arg in rads */
    function degrees(arg) {
        return (arg / de2ra);
    }

    /** brief Arccosine implementation.
    *
    * Returns a value between zero and two pi.
    * Borrowed from gsat 0.9 by Xavier Crehueras, EB3CZS.
    * Optimized by Alexandru Csete.
    */
    function arccos(x, y) {
        if (x && y) {
            if (y > 0.0) {
                return Math.acos(x / y);
            }
            else if (y < 0.0) {
                return pi + Math.acos(x / y);
            }
        }

        return 0.0;
    }

    function get_orbits(satrec, t) {
        /**
         * Calculate 300 orbital points with 60 second increments, starting at epoch t
         *
         * @return {Array} Array that contains Arrays of geodetic (lon, lat) pairs in degrees
         */

        // Number of positions to compute
        const COUNT = 300;

        // Interval in ms between positions to compute
        const STEP = 60*1000;

        // Create satellite orbit
        var current_orbit = [];
        var all_orbits = [];

        var previous = 0;
        for ( var i = 0; i < COUNT; i++) {
            const coords = calc_geodetic_coords(satrec, t) ;

            if (Math.abs(coords['lon'] - previous) > 180) {
                // Satellite passed the 180th meridian.
                // Save last orbital point and
                // start new Array for the next orbit
                current_orbit.push([coords['lon']+360, coords['lat']]);
                all_orbits.push(current_orbit);
                current_orbit = [];
            }

            current_orbit.push([coords['lon'], coords['lat']]);
            previous = coords['lon'];

            // Increase time for next point
            t.setTime(t.getTime() + STEP);
        }
        return all_orbits;
    }

    function calc_geodetic_coords(satrec, t) {
        const positionAndVelocity = satellite.propagate(satrec, t);
        const gmst = satellite.gstime(t);
        const positionEci = positionAndVelocity.position;
        const positionGd = satellite.eciToGeodetic(positionEci, gmst);
        const longitude = satellite.degreesLong(positionGd.longitude);
        const latitude  = satellite.degreesLat(positionGd.latitude);

        return {'lon': longitude,
            'lat': latitude,
            'height': positionGd.height};
    }

    function get_range_circle(current_coords) {
        // first we have to calculate the footprint
        var footprint = 12756.33 * acos (earthRadius / (earthRadius+current_coords.height));

        var azi,
            ssplat,
            ssplon,
            beta,
            azimuth,
            num,
            dem;

        /* Range circle calculations.
         * Borrowed from gsat 0.9.0 by Xavier Crehueras, EB3CZS
         * who borrowed from John Magliacane, KD2BD.
         * Optimized by Alexandru Csete and William J Beksi.
         */
        ssplat = radians(current_coords.lat);
        ssplon = radians(current_coords.lon);
        beta = (0.5 * footprint) / earthRadius;

        var points = [];
        var lat = 0.0;
        var lon = 0.0;

        for (azi = 0; azi < 360; azi += 5) {
            azimuth = de2ra * azi;
            lat = asin(sin(ssplat) * cos(beta) + cos(azimuth) * sin(beta)
                    * cos(ssplat));
            num = cos(beta) - (sin(ssplat) * sin(lat));
            dem = cos(ssplat) * cos(lat);

            if (azi == 0 && (beta > pio2 - ssplat)) {
                lon = ssplon + pi;
            }
            else if (azi == 180 && (beta > pio2 + ssplat)) {
                lon = ssplon + pi;
            }
            else if (fabs(num / dem) > 1.0) {
                lon = ssplon;
            } else {
                if ((180 - azi) >= 0) {
                    lon = ssplon - arccos(num, dem);
                } else {
                    lon = ssplon + arccos(num, dem);
                }
            }
            points.push([degrees(lon), degrees(lat)]);
        }
        return points;
    }

    // Load satellite orbit data from TLE
    var satrec = satellite.twoline2satrec(tle1, tle2);


    // Calculate orbits and current satellite location
    const now = new Date();
    var current_coords = calc_geodetic_coords(satrec, now);
    var sat_location = [current_coords.lon, current_coords.lat];
    var footprint = get_range_circle(current_coords);

    var all_orbits = get_orbits(satrec, now);

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/cshields/ckc1a24y45smb1ht9bbhrcrk6',
        zoom: 2,
        center: sat_location
    });

    map.addControl(new mapboxgl.NavigationControl());

    map.on('load', function () {

        map.loadImage('/static/img/satellite-marker.png', function(error, image) {
            map.addImage('sat_icon', image);
        });


        var location_data = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': sat_location
                }
            }]
        };

        map.addSource('sat_location', {
            'type': 'geojson',
            'data': location_data
        });

        map.addLayer({
            'id': 'sat_location',
            'type': 'symbol',
            'source': 'sat_location',
            'layout': {
                'icon-image': 'sat_icon',
                'icon-size': 0.4
            }
        });

        var orbit_data = {
            'type': 'FeatureCollection',
            'features': []
        };

        all_orbits.forEach(function(orbit){
            orbit_data.features.push({
                'type': 'Feature',
                'geometry': {
                    'type': 'LineString',
                    'coordinates': orbit
                }
            });
        });

        map.addSource('sat_orbit', {
            'type': 'geojson',
            'data': orbit_data
        });

        map.addLayer({
            'id': 'sat_orbit',
            'type': 'line',
            'source': 'sat_orbit'
        });

        var footprint_data = {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [footprint]
                }
            }]
        };

        map.addSource('sat_footprint', {
            'type': 'geojson',
            'data': footprint_data
        });

        map.addLayer({
            'id': 'sat_footprint',
            'type': 'fill',
            'source': 'sat_footprint',
            'paint': {
                'fill-opacity': 0.2
            }
        });

        function update_map() {
            // Recalculate current satellite location
            current_coords = calc_geodetic_coords(satrec, new Date());
            sat_location = [current_coords.lon, current_coords.lat];
            footprint = get_range_circle(current_coords);
            location_data.features[0].geometry.coordinates = sat_location;
            footprint_data.features[0].geometry.coordinates = [footprint];
            map.getSource('sat_location').setData(location_data);
            map.getSource('sat_footprint').setData(footprint_data);
        }
        setInterval(update_map, 5000);
    });

    // couldn't get this to work with shown.bs.tab, have to go with click
    // timeout is necessary for the first click for some reason
    document.getElementById('mapcontent-tab').addEventListener('click', function() {
        setTimeout( function() { map.resize();}, 200);
    });
    // for deep-linking of satellite tab anchors 
    $('#mapcontent-tab').on('shown.bs.tab', function() {
        setTimeout( function() { map.resize();}, 200);
    });
});
