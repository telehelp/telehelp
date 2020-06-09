import React from "react";

const Press = () => {
  const mediaApperance = [
    {
      title: "Vinnare av Hack The Crisis",
      media: "Hack the Crisis pressmeddelande",
      date: "2020-04-06",
      link:
        "https://www.mynewsdesk.com/se/hack-for-sweden/pressreleases/winners-of-hack-the-crisis-2989133",
      description: "Vinnare i kategorin Digital - Save Communities",
    },
    {
      title: "Hoppfulla resultat av Hack the Crisis",
      media: "KTH aktuellt",
      date: "2020-04-08",
      link:
        "https://www.kth.se/aktuellt/nyheter/hoppfulla-resultat-av-hack-the-crisis-1.973649",
      description: "",
    },
    {
      title: "Telehelp en av vinnarna i svenska ”Hack the crisis”",
      media: "Digital hälsa",
      date: "2020-04-08",
      link:
        "https://app.red.bbmbonnier.se/e/es?s=355424421&e=913550&elqTrackId=aab2e8d998ac428ab064b29999b8fa67&elq=3301dc131494412b98482696742f133e&elqaid=32630&elqat=1",
      description: "",
    },
    {
      title: "Nystartad hjälptelefon ska stötta äldre i krisvardagen",
      media: "Mitti Stockholm",
      date: "2020-04-15",
      link: "https://mitti.se/nyheter/nystartad-hjalptelefon-krisvardagen/",
      description: "",
    },
    {
      title: "Telehelp – bridging the digital divide",
      media: "Cybercom News",
      date: "2020-05-05",
      link: "https://www.cybercom.com/About-Cybercom/Press-Media/News/telehelp/",
      description: "",
    },
  ];

  return (
    <div>
      <header className="tele-header-small">
        <div className="container">
          <h1 className="tele-title">I media</h1>
        </div>
      </header>
      <section className="tele-section">
        <div className="container">
          <div className="row">
            <div className="col-lg-12">
              {mediaApperance.map((e, i) => {
                return (
                  <div className="media-entry" key={i}>
                    <h5>{e.date}</h5>
                    <a href={e.link}>
                      <h3>{e.title}</h3>
                    </a>
                    <strong>{e.media}</strong>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Press;
