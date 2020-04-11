import React from "react";

const About = () => {
  const people = [
    {
      name: "David",
      responsibility: "Webmaster",
      about: "Studies electrical engineering and robotics at KTH",
      email: "david@telehelp.se",
    },
    {
      name: "Daniel Eriksson",
      responsibility: "System administrator",
      about: "Electrical engineer at SAAB",
      email: "daniel@telehelp.se",
    },
    {
      name: "Johan Ehrenfors",
      responsibility: "Backend developer",
      about: "Consultant for Ericsson through Cybercom",
      email: "johan@telehelp.se",
    },
    {
      name: "Therese Persson",
      responsibility: "Backend developer",
      about: "Data engineer at Sellpy",
      email: "therese@telehelp.se",
    },
    {
      name: "Dennis Lioubartsev",
      responsibility: "Chief Creative Designer",
      about: "BSc Product Realization, MSc Mechatronics",
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
    </div>
  );
};

export default About;
