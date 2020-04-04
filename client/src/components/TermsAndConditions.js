import React from 'react';

class TermsAndConditions extends React.Component{
    render () {
        const terms = ["Du kan när som helst gå ur tjänsten genom att ta bort ditt nummer på samma ställe som du registrerade dig.",
                        "Pensionärers telefonnummer kommer automatiskt att raderas ur databasen efter fyra veckors inaktivitet, men självklart är personen välkommen att använda tjänsten igen om detta skulle ha skett - men det kanske inte blir med samma volontär!",
                        "Vi tar ej ansvar vid eventuella tvister mellan tjänstens användare.",
                        "Något om PuL också kanske"]
        return (
            <div className="terms" id="terms">
                <h2>Användarvillkor</h2>
                <ul>
                    {terms.map((element, i) => {
                        return <li key={i}>{element}</li>
                    })}
                </ul>
            </div>
        )
    }
}
export default TermsAndConditions;


