import React from "react";

const CrashNotice = () => {
  return (
    <div className="crash-notice">
      <h2>Registrera dig även om du redan gjort det!</h2>
      <p>
        Natten till den 16 april förlorade vi de flesta användare i en
        serverkrasch, och vår databas gick tyvärr inte att återställa. Vi har
        jobbat hårt med att utöka funktionaliten de senaste dagarna och
        backuprutiner var en av många saker på den listan. Dessa rutiner är nu
        på plats, om än något sent, för att något liknande aldrig ska hända
        igen. Vi vill också passa på att tacka er nära 100 användare som
        hittills har registrerat er och bara är ett telefonsamtal ifrån de som
        behöver er hjälp.
      </p>
    </div>
  );
};

export default CrashNotice;
