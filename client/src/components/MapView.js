import React from 'react'
import { Map as LeafletMap, TileLayer, Marker} from 'react-leaflet';
//Popup?

class MapView extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      addressPoints: [],
    }
  }

  componentDidMount() {
    var coords = [[59.321051789769314, 16.321737535467456],
    [59.275588587351294, 14.486207028120337],
    [59.37369677817046, 17.508152603775272],
    [59.916272261266286, 16.67993249677571],
    [59.93814298452618, 16.830169410292186],
    [59.105474614358165, 16.957269799759676],
    [59.848795793769895, 15.854128761257623],
    [59.29680160598779, 14.111367426995375],
    [59.19858583036644, 15.084658344714647],
    [59.77187531791105, 15.648861742350167],
    [59.33965228399058, 17.465079457902384],
    [59.13753718107035, 16.60113149859169],
    [59.51413399422899, 15.26232588963046],
    [59.41619330490079, 14.071382855318332],
    [59.85572664831179, 15.745807772281768]]

    fetch('/getVolunteerLocations')
    .then(res => res.json())
    .then(data => {
      this.setState({addressPoints: data.coordinates});
      })
    .catch(console.log('error fetching coords, using defaults'))
    
    if (this.state.addressPoints.length === 0)
    {
      this.setState({addressPoints: coords});
    }
  }

  render() {
    const {addressPoints} = this.state;

    return (
      <div className="mapHolder">
        <h2>Våra {addressPoints.length} st volontärer finns i hela landet</h2>
      <div id="mapid" className="leaflet-container">
        <LeafletMap
          center={[59.73, 17.4]}
          zoom={7}
          maxZoom={20}
          attributionControl={true}
          zoomControl={true}
          doubleClickZoom={true}
          scrollWheelZoom={true}
          dragging={true}
          animate={true}
          easeLinearity={0.35}
        >
          <TileLayer
            url='https://{s}.tile.osm.org/{z}/{x}/{y}.png'
          />

          {addressPoints.map((e, i) => {
            return <Marker key={i} position={[e[0], e[1]]}></Marker>
          })}
        </LeafletMap>
      </div>
      </div>
    );
  }
}

export default MapView
