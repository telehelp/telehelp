import React from "react";

const CrashNotice = () => {
  return (
    <div class="alert alert-info" role="alert">
      <h3 class="alert-heading">Till er som registrerat er som volontärer</h3>
      <p>
        Natten till den 16 april kraschade vår server, och vår databas med era uppgifter gick tyvärr inte att återställa. Vi har jobbat hårt med att utöka funktionaliten de senaste dagarna och backuprutiner var en av många saker på den listan. Dessa rutiner är nu på plats, om än något sent, för att något liknande aldrig ska hända igen. <strong>Därför får vi be er som redan registrerat er, att registrera er igen.</strong> Tack för att ni vill vara med och göra en insats för de som behöver hjälp!
      </p>
    </div>
  );
};

export default CrashNotice;
