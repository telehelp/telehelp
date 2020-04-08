import React from 'react'

const About = () => {
    const people = [
        {
            "name": "David",
            "responsibility": "Webmaster",
            "about": "Studerar elektroteknik och robotik vid KTH",
            "email": "david@telehelp.se"
        },
        {
            "name": "Johan Ehrenfors",
            "responsibility": "Backend developer",
            "about": "Konsult åt Ericsson hos Cybercom",
            "email": "johan@telehelp.se"
        },
        {
            "name": "Therese Persson",
            "responsibility": "Backend developer",
            "about": "Data engineer hos Sellpy",
            "email": "therese@telehelp.se"
        }
    ]
    return (
        <div>
            {people.map((e, i) => {
                return <div key={i}>
                        <h3>{e.name}</h3>
                        <h4>{e.responsibility}</h4>
                        <p>{e.about}</p>
                        Kontakt: <a href={"mailto:" + e.email}>{e.email}</a>
                    </div>
            })}
        </div>
    )
}

export default About
