import React from 'react'

const About = () => {
    const people = [
        {
            "name": "David",
            "responisbility": "Webmaster",
            "about": "Studerar elektroteknik och robotik vid KTH",
            "email": "david@telehelp.se"
        }
    ]
    return (
        <div>
            {people.map((e, i) => {
                return <div key={i}>
                        <h3>{e.name}</h3>
                        <h4>{e.responisbility}</h4>
                        <p>{e.about}</p>
                        Kontakt: <a href={"mailto:" + e.email}>{e.email}</a>
                    </div>
            })}
        </div>
    )
}

export default About