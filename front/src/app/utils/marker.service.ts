import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import * as L from 'leaflet';
import { PopupService } from "./popup.service";
import { Point } from "./model/point";

@Injectable({
  providedIn: 'root'
})
export class MarkerService {
  capitals: string = 'assets/data/usa-capitals.geojson'
  data_p1: string = 'assets/data/coordonnes.json'
  marker?: L.Marker;
  line?: L.Polyline;
  constructor(private http: HttpClient, private popUpService: PopupService) { }

  makeMarkers(map: L.Map, point:Point) {
    const lon = point.longitude;
    const lat = point.latitude;
    if(this.marker){
      map.removeLayer(this.marker)
    }
    this.marker = L.marker([lon, lat]);

    this.marker.bindPopup(this.popUpService.makePopUp(point))

    this.marker.addTo(map);
  }

  makePath(map: L.Map, points: any[]){
    if( this.line) {
      map.removeLayer(this.line)
    }
    this.line = L.polyline(points, {color: 'red', weight: 2, dashArray: '10 10', lineJoin:'round'})
    this.line.addTo(map)
  }
  afficherMarkerIP(map: L.Map, point:Point) {
    /*
    Requete l'API pour la liste des coordonnées d'un produceur
     */

    this.http.get(`http://localhost:8000/coordonnees/${point.ip}`).subscribe((res: any) => {
      this.makeMarkers(map, point)
      let points = []
      for(const point of res) {
        points.push([point.longitude, point.latitude])
      }
      this.makePath(map, points)

    })
  }
  /*usaMarkers(map: L.Map) {
    this.http.get(this.capitals).subscribe((res:any)=> {
      this.makeMarkers(map, res.features[0])
      let points = []
      for(const point of res.features) {
        points.push([
          point.geometry.coordinates[1], point.geometry.coordinates[0]
        ])
      }
      console.log(points)

     points = [
        [45.51, -122.68],
        [37.77, -122.43],
        [34.04, -118.2]
      ];
      this.makePath(map, points)
    })
  }*/
}
