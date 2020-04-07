import React from 'react'

class ThanksTo extends React.Component {
  render() {
    const sponsors = [{"link": "https://46elks.se/", "imagePath": "img/46elks-logo.svg"},
                {"link": "https://cybercom.com", "imagePath": "img/cybercom-logo.svg"}
                ];
    
    return (
    <div className="row">
          {sponsors.map((e,i) => {
              return <div key={i} className="col-md-2">
                  <a href={e.link}><img className="img-fluid sponsor-image" src={e.imagePath} style={{"margin": "1em"}} alt="sponsor logo"/></a>
                  </div>
          })}
      </div>
    );
  }
}

export default ThanksTo;
