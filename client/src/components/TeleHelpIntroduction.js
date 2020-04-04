import React from 'react';

class TeleHelpIntroduction extends React.Component{
//     <div className="col-4 text-left">
//     <img className="photo" src="/old-people.png" alt="Two happy old people on a bench"></img>
// </div>
    render () {
        return (
            <div className="introduction">
                <h2>Få hjälp av dina grannar att klara vardagen</h2>

                <div className="row">
                <div className="col-7">
                <p>
                    Som riskgrupp kan du ringa numret nedan för att enkelt få hjälp med dina vargadsbestyr av en voluntär i närheten.
                </p>
                <h1>TeleHelp: <a href="+46766861551">07666861551</a></h1>
                </div>

              </div>
                
            </div>
        )
    }
}
export default TeleHelpIntroduction;


