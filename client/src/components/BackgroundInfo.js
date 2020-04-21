import React from "react";

const BackgroundInfo = () => {
  return (
    <div className="introduction">
      <h2>Bli en vardagshjälte idag</h2>
      <p>
        Genom att anmäla dig som volontär där du bor kan personer som ingår i
        riskgrupper eller som redan är smittade av corona vår vår tjänst komma i
        kontakt med dig för att få hjälp med sysslor som plötsligt blivit svåra
        på grund av coronakrisen, exempelvis att handla mat eller hämta ut
        mediciner.
      </p>
      <img
        className="img-fluid"
        src="/img/old-people.png"
        alt="Two happy old people on a bench"
      ></img>
    </div>
  );
};

export default BackgroundInfo;
