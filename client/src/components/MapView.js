import React from 'react'
import { Map as LeafletMap, TileLayer, Marker, Popup } from 'react-leaflet';

class MapView extends React.Component {
  render() {
    var addressPoints = [
      [59.321051789769314, 16.321737535467456, '0'],
      [59.275588587351294, 14.486207028120337, '1'],
      [59.37369677817046, 17.508152603775272, '2'],
      [59.916272261266286, 16.67993249677571, '3'],
      [59.93814298452618, 16.830169410292186, '4'],
      [59.105474614358165, 16.957269799759676, '5'],
      [59.848795793769895, 15.854128761257623, '6'],
      [59.29680160598779, 14.111367426995375, '7'],
      [59.19858583036644, 15.084658344714647, '8'],
      [59.77187531791105, 15.648861742350167, '9'],
      [59.33965228399058, 17.465079457902384, '10'],
      [59.13753718107035, 16.60113149859169, '11'],
      [59.51413399422899, 15.26232588963046, '12'],
      [59.41619330490079, 14.071382855318332, '13'],
      [59.85572664831179, 15.745807772281768, '14'],
      [59.15663909018626, 18.33879023152591, '15'],
      [59.31385382082655, 15.13752595517913, '16'],
      [59.11892866243675, 15.81442752950803, '17'],
      [59.48978441279864, 16.012019884355354, '18'],
      [59.879306828997166, 17.50250122394378, '19'],
      [59.098295051207245, 15.069611830136603, '20'],
      [59.48780542465078, 17.76004619616242, '21'],
      [59.20657591288641, 16.11775128368165, '22'],
      [59.91977032849383, 17.567395437149948, '23'],
      [59.814172970910754, 15.635446433974439, '24'],
      [59.40214342053156, 14.678957870133313, '25'],
      [59.35446418457809, 17.083448816776798, '26'],
      [59.555499836121804, 16.776627303470114, '27'],
      [59.289011372040285, 15.455517853977216, '28'],
      [59.74095565528755, 16.251773922070758, '29'],
      [59.959505408437174, 15.114652726009364, '30'],
      [59.45927728804888, 18.299840139750522, '31'],
      [59.86249504031554, 14.981397140033971, '32'],
      [59.77819750131587, 15.938474036826248, '33'],
      [60.011919744367155, 16.30445229233517, '34'],
      [59.5157894782395, 17.322805707638974, '35'],
      [59.86946970570576, 14.857774288707763, '36'],
      [59.03917769437227, 17.15153243292137, '37'],
      [59.553704074611616, 15.70694102149045, '38'],
      [59.590887068656805, 14.573331116859226, '39'],
      [59.80465355153128, 14.482649238786756, '40'],
      [59.06755580637579, 16.578163248392382, '41'],
      [59.16807946553017, 16.326201794722916, '42'],
      [59.90106014457416, 16.697484017334745, '43'],
      [59.743443772474734, 16.09485270658825, '44'],
      [59.66660534428229, 15.2324186760242, '45'],
      [59.63977767166157, 14.35393065946813, '46'],
      [59.03999432458846, 16.715961646929248, '47'],
      [59.8842252497492, 15.228192071530204, '48'],
      [59.68556821071719, 14.800068923224572, '49'],
      [59.29648696122155, 14.666063341083877, '50'],
      [59.994313403966736, 18.062052724943545, '51'],
      [59.06847629955238, 14.173805738343527, '52'],
      [59.36633371070398, 18.08989346553173, '53'],
      [59.8020308216581, 16.229213507712462, '54'],
      [59.28197392178578, 14.809118136096256, '55'],
      [60.01907054844075, 15.95504815034623, '56'],
      [59.64405024296973, 17.267502813526992, '57'],
      [60.00023703958818, 18.300594319298003, '58'],
      [59.736377998553486, 15.527675705282936, '59'],
      [59.812251720323935, 15.322137118143397, '60'],
      [59.06276815909209, 14.52340330242728, '61'],
      [59.03550518348323, 17.29313378926754, '62'],
      [59.32286364648903, 16.364623474012568, '63'],
      [59.286307413896196, 17.3048096804511, '64'],
      [59.07541981168234, 15.289335939053696, '65'],
      [60.000464760138094, 17.768965752317868, '66'],
      [59.26511137769831, 14.465823831220302, '67'],
      [59.120143147062095, 15.499311039313252, '68'],
      [59.95383051238838, 16.755495042513374, '69'],
      [59.83654303220111, 17.163571201557545, '70'],
      [59.53239191884112, 16.601561405806848, '71'],
      [59.37120691729519, 16.465775070741817, '72'],
      [59.61136666964467, 14.322244774968842, '73'],
      [59.567573017724634, 14.164324862457427, '74'],
      [59.961750343804, 15.949676086531735, '75'],
      [59.74822713600682, 17.153747475512084, '76'],
      [59.90053838574901, 18.11497035154811, '77'],
      [59.54632099198832, 15.991742546773848, '78'],
      [59.88664572794601, 15.228792488633713, '79'],
      [59.17021349146649, 16.85668196938012, '80'],
      [59.56918662341024, 18.264996520816503, '81'],
      [59.79962664020857, 14.967375646473162, '82'],
      [59.13628367447899, 15.48373145970217, '83'],
      [59.073941676048, 16.86269810706643, '84'],
      [59.60418654503079, 16.392504442674642, '85'],
      [59.19968350475739, 17.43622287275371, '86'],
      [59.61541160334489, 16.657197517025068, '87'],
      [59.65697208723597, 17.64658621936694, '88'],
      [59.035655508418465, 17.472513522198312, '89'],
      [59.857730865224895, 15.845201176673605, '90'],
      [59.9705971377229, 14.215426121250381, '91'],
      [59.23758111617859, 14.653529514968984, '92'],
      [59.070167093614565, 16.974442307033915, '93'],
      [59.34647171666439, 17.942230043054614, '94'],
      [59.6318409314752, 17.50191800092042, '95'],
      [59.90791120974043, 17.238601071712843, '96'],
      [59.23618723462516, 15.183110806836702, '97'],
      [59.72232229300064, 15.236942540536049, '98'],
      [59.66318740793199, 18.022921781795475, '99']
      ]

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

          {addressPoints.map(e => {
            return <Marker position={[e[0], e[1]]}><Popup>{e[2]}</Popup></Marker>
          })}
        </LeafletMap>
      </div>
      </div>
    );
  }
}

export default MapView
