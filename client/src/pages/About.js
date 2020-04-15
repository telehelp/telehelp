import React from "react";

const About = () => {
  const people = [
    {
      name: "David Ekvall",
      responsibility: "Frontend developer",
      about: "Studerar elektroteknik och robotik vid KTH",
      email: "david@telehelp.se",
    },
    {
      name: "Johan Ehrenfors",
      responsibility: "Backend developer",
      about: "Konsult åt Ericsson hos Cybercom",
      email: "johan@telehelp.se",
    },
    {
      name: "Therese Persson",
      responsibility: "Backend developer",
      about: "Data engineer hos Sellpy",
      email: "therese@telehelp.se",
    },
    {
      name: "Daniel Eriksson",
      responsibility: "System administrator",
      about: "Elektroingenjör på SAAB",
      email: "daniel@telehelp.se",
    },
    {
      name: "Dennis Lioubartsev",
      responsibility: "Chief Creative Designer",
      about: "Civilingenjör i mekatronik",
      email: "dennis@telehelp.se",
    },
  ];
  return (
    <div>
      {people.map((e, i) => {
        return (
          <div key={i} className="about-entry">
            <h3>{e.name}</h3>
            <h4>{e.responsibility}</h4>
            <p>{e.about}</p>
            Kontakt: <a href={"mailto:" + e.email}>{e.email}</a>
          </div>
        );
      })}
      <img
        className="img-fluid about-image"
        src="/img/all-of-us.jpg"
        alt="The telehelp team"
      />
    </div>
  );
};

export default About;
