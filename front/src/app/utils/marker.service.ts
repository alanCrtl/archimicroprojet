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

  layers: {marker:L.Marker, path: L.Polyline, point: Point}[] = []

  constructor(private http: HttpClient, private popUpService: PopupService) { }

  makeMarkers(map: L.Map, point:Point): L.Marker {
    const lon = point.longitude;
    const lat = point.latitude;
    const marker = L.marker([lon, lat]);

    marker.bindPopup(this.popUpService.makePopUp(point))
    return marker
  }

  makePath(map: L.Map, points: any[]): L.Polyline{
    return L.polyline(points, {color: 'red', weight: 2, dashArray: '10 10', lineJoin:'round'})
  }
  afficherMarkerIP(map: L.Map, point:Point) {
    /*
    Requete l'API pour la liste des coordonnées d'un produceur
     */
    let exist = false;
    let index = this.layers.length

    for (let i = 0; i <this.layers.length ; i++) {
      if( this.layers[i].point.ip===point.ip){
        exist = true
        index = i
      }
    }

    this.http.get(`http://localhost:8000/coordonnees/${point.ip}`).subscribe((res: any) => {
      const marker = this.makeMarkers(map, point)
      let points = []
      for(const point of res) {
        points.push([point.longitude, point.latitude])
      }
      const path=  this.makePath(map, points)

      if(exist){
        map.removeLayer(this.layers[index].marker)
        map.removeLayer(this.layers[index].path)
        this.layers[index].marker = marker
        this.layers[index].point = point
        this.layers[index].path = path
      } else {
        this.layers.push({
          marker,
          path,
          point
        })
      }

      this.layers[index].marker.addTo(map)
      this.layers[index].path.addTo(map)

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
