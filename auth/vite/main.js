import Map from 'ol/Map';
import View from 'ol/View';
import OSM from 'ol/source/OSM';
import TileLayer from 'ol/layer/Tile';
import Source from 'ol/source/Vector';
import Layer from 'ol/layer/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import Style from 'ol/style/Style';
import Circle from 'ol/style/Circle';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import MultiPoint from 'ol/geom/MultiPoint';
import {buffer} from 'ol/extent';
import proj4 from 'proj4';

const url = 'https://api.nyc.gov/geoclient/v2/search';

const form = document.getElementById('search-form');

const view = new View({
  center: [-8235252, 4969073],
  zoom: 9
});

const locationLayer = new Layer();

const locationStyle = new Style({
  image: new Circle({
    fill: new Fill({color: 'rgba(	255, 69, 0, .6)'}),
    stroke: new Stroke({width: 2, color: 'rgb(	255, 69, 0)'}),
    radius: 8
  })
});

const map = new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new OSM(),
    }),
    locationLayer
  ],
  view: view
});

const getLocation = geocodeResult => {
  let locationCoordinate;
  let longitude = geocodeResult.longitudeInternalLabel;
  let latitude = geocodeResult.latitudeInternalLabel;
  if (longitude !== undefined && latitude !== undefined) {
    locationCoordinate = [longitude, latitude]
  } else {
    let longitude = geocodeResult.longitude;
    let latitude = geocodeResult.latitude;
    if (longitude !== undefined && latitude !== undefined) {
      locationCoordinate = [geocodeResult.longitude * 1, geocodeResult.latitude * 1];
    }
  }
  if (locationCoordinate === undefined) {
    throw({error: 'location coordinate not found in response', geocodeResult})
  }
  return proj4('EPSG:4326', 'EPSG:3857', locationCoordinate);
}

const mapLocations = locations => {
  const locationSource = new Source({});  
  const multiPoint = new MultiPoint([]);
  locations.forEach(location => {
    const locationCoordinate = getLocation(location.response);
    const point = new Point(locationCoordinate);
    multiPoint.appendPoint(point);
    const locationFeature = new Feature({
      geometry: point,
      geocodeResult: location.response
    });
    locationFeature.setStyle(locationStyle);
    locationSource.addFeature(locationFeature);
  });
  locationLayer.setSource(locationSource);
  if (locations.length == 1) {
    view.setCenter(multiPoint.getCoordinates()[0]);
    view.setZoom(17);  
  } else {
    view.fit(buffer(multiPoint.getExtent(), 1000), {size: map.getSize()});
  }
}

const displayGeoClientResponse = geoClientResponse => {
  const json = JSON.stringify(geoClientResponse, null, 2);
  document.getElementById('geoclient-response').innerHTML = json;
}

const displayError = error => {
  if (error.json) error = error.json();
  document.getElementById('geoclient-response').innerHTML = error;
}

const handleGeoClientResponse = geoClientResponse => {
  displayGeoClientResponse(geoClientResponse);
  const results = geoClientResponse.results;
  if (results.length > 0) {
    mapLocations(results);
  } else {
    alert(`"${form.input.value}" not found.`);
  }
}

const submit = event => {
  event.preventDefault();

  fetch(`${url}?input=${form.input.value}`, {
    method: 'GET',
    headers: {
      'Ocp-Apim-Subscription-Key': form.key.value,
      'Cache-Control': 'no-cache'
    }
  }).then(response => {
    response.json().then(handleGeoClientResponse);
  }).catch(displayError);

}

form.addEventListener('submit', submit);
