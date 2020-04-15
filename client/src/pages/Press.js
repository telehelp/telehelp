import React from "react";

const Press = () => {
  const mediaApperance = [
    {
      header: "Vinnare av Hack The Crisis 2020",
      name: "Hack the Crisis pressmeddelande",
      link:
        "https://www.mynewsdesk.com/se/hack-for-sweden/pressreleases/winners-of-hack-the-crisis-2989133",
      description:
        "Det var några långa dagar och nätter, men det gick bra tillslut",
    },
    {
      header: "KTH aktuellt",
      name: "Hoppfulla resultat av Hack the Crisis",
      link:
        "https://www.kth.se/aktuellt/nyheter/hoppfulla-resultat-av-hack-the-crisis-1.973649",
      description:
        "Tyvärr är bara en av oss med i artikeln, trots att alla gjorde ett fantastiskt arbete",
    },
    {
      header: "Digital hälsa",
      name: "Telehelp en av vinnarna i svenska ”Hack the crisis”",
      link:
        "https://app.red.bbmbonnier.se/e/es?s=355424421&e=913550&elqTrackId=aab2e8d998ac428ab064b29999b8fa67&elq=3301dc131494412b98482696742f133e&elqaid=32630&elqat=1",
      description:
        "Återigen är bara en av oss med i artikeln, men vi hoppas på en samlad intervju i framtiden",
    },
    {
      header: "Mitti Stockholm",
      name: "Nystartad hjälptelefon ska stötta äldre i krisvardagen",
      link: "https://mitti.se/nyheter/nystartad-hjalptelefon-krisvardagen/",
      description:
        "En bild på oss alla (nästan) tillsammans och en härligt skriven artikel",
    },
  ];

  return (
    <div>
      {mediaApperance.map((e, i) => {
        return (
          <div key={i}>
            <h3>{e.header}</h3>
            <a href={e.link}>{e.name}</a>
            <p>{e.description}</p>
          </div>
        );
      })}
    </div>
  );
};

export default Press;
