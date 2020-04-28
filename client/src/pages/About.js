import React from "react";
import MissionStatement from "../components/MissionStatement";

const About = () => {
  const people = [
    {
      name: "Johan Ehrenfors",
      responsibility: "Backend developer",
      about: "Konsult åt Ericsson hos Cybercom",
      email: "johan@telehelp.se",
      img: "img/team/Johan.png",
    },
    {
      name: "Therese Persson",
      responsibility: "Backend developer",
      about: "Data engineer hos Sellpy",
      email: "therese@telehelp.se",
      img: "img/team/Therese.png",
    },
    {
      name: "David Ekvall",
      responsibility: "Frontend developer",
      about: "Studerar elektroteknik och robotik vid KTH",
      email: "david@telehelp.se",
      img: "img/team/David.png",
    },
    {
      name: "Daniel Eriksson",
      responsibility: "System administrator",
      about: "Elektroingenjör på SAAB",
      email: "daniel@telehelp.se",
      img: "img/team/Daniel.png",
    },
    {
      name: "Dennis Lioubartsev",
      responsibility: "Chief Creative Designer",
      about: "Civilingenjör i mekatronik",
      email: "dennis@telehelp.se",
      img: "img/team/Dennis.png",
    },
    {
      name: "Sara Danielsson",
      responsibility: "Desiger/Frontend Developer",
      about: "Civilingenjör i teknisk fysik",
      email: "sara@telehelp.se",
      img: "img/team/Sara.png",
    },
  ];
  return (
    <div>
      <header className="tele-header-small">
        <div className="container">
          <h1 className="tele-title">Om oss</h1>
        </div>
      </header>
      <section className="text-center">
        <div className="container">
          <div className="row">
            <div className="col-lg-12">
              <MissionStatement />
            </div>
          </div>
        </div>
      </section>
      <section>
        <div className="container">
          <h2 className="text-center">Vi bakom Telehelp</h2>
          <div className="row">
            {people.map((e, i) => {
              return (
                <div className="col-lg-4" key={i}>
                  <div key={i} className="about-entry">
                    <img
                      className="img-fluid about-entry-img"
                      src={e.img}
                      alt={e.name}
                    />
                    <h3>{e.name}</h3>
                    <h4>{e.responsibility}</h4>
                    <p>{e.about}</p>
                    <a href={"mailto:" + e.email}>{e.email}</a>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
};

export default About;
