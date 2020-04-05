import React from 'react';
import { UncontrolledCollapse, Button } from 'reactstrap';

class FAQ extends React.Component{

    render () {
        const zip = (arr1, arr2) => arr1.map((k, i) => [k, arr2[i]]);

        // const questions = ["Hur fungerar det?",
        //                 "Hur finansieras tjänsten?",
        //                 "Kan jag hjälpa mer än en pensionär?",
        //                 "Vad gör detta för att underlätta coronakrisen?",
        //                 "Kan jag lita på att ni hanterar min data på ett bra sätt?",
        //                 "Hur drar jag mig ur rollen som volontär?",
        //                 "Hur ska vi hantera betalningar och leveranser?"]

        // const answers = ["När du skriver upp dig som volontär ber vi dig att uppge ditt tilltalsnamn, telefonnummer, och postnummer. När en hemmasittande person ringer upp Telehelp kommer de att själva uppge sitt postnummer, och kopplas därefter ihop med volontärer i närområdet. Om du blir uppringd kommer ni att få gemensamt bestämma hur ni vill hantera ärendet - Telehelp står bara för att etablera kontakten. Om du eller pensionären själv ringer upp det nummer du blivit uppringd ifrån, kommer ni automatiskt att bli ihopkopplade - på så vis måste ni inte skriva ner några telefonnummer till varandra.",
        //                 "Detta projekt startades under Hack The Crisis, ett initiativ från svenska regeringen, lett av Myndigheten för Digital Förvaltning (DIGG). <se: www.hackthecrisis.se/ > Vi och våra sponsorer/tredjepartsverktyg (46elks, AWS, Google Cloud, Domainkiosk/nameisp, etc) står i dagsläget för alla driftskostnader, men vi kommer öppna för donationer vid behov. Hör gärna av dig på info@telehelp.se",
        //                 "För att minimera smittorisken och förenkla användarupplevelsen är tjänsten byggd för att du ska kunna paras ihop med en enda person i riskgruppen i taget. Pensionären kan när som helst välja att byta till en annan volontär, vartefter ni inte längre kan komma i kontakt. Även du själv kan ta bort ditt konto om du inte längre vill använda tjänsten, men vi rekommenderar att du förklarar detta för den du hjälper först.",
        //                 "Enligt Folkhälsomyndigheten (se: https://omni.se/folkhalsomyndighetens-nya-rad-aldre-bor-undvika-mataffarer-helt-och-hallet/a/Vb8PjW) bör inte personer som tillhör riskgrupper besöka matvarubutiker om de kan undvika detta, för att minimera antalet hårt drabbade av viruset.",
        //                 "Vi har gjort vårt bästa för att hitta en lösning som kräver så lite personlig information om både personerna i riskgrupp och volontärer som möjligt: endast ett telefonnummer och en postkod. Ett tilltalsnamn används också för att göra tjänsten mer personlig. Den som använder tjänsten får aldrig reda på den andra personens telefonnummer, och kan när som helst avbryta möjligheten till kommunikation till och från den andra parten.",
        //                 "Om du känner dig helt säker på att du inte vill vara en vardagshjälte, så kan du antingen ringa upp numret själv och följa instruktionerna, eller maila oss för att vi ska ta bort ditt telefonnummer manuellt ur vår databas. Om du redan har kontakt med en pensionär rekommenderar vi att du förklarar varför du inte längre kan hjälpa till innan du gör detta.",
        //                 "Telehelp bidrar endast med att knyta samman pensionärer och volontärer. Det är upp till er att gemensamt hitta en lösning som fungerar för båda parter. Vi rekommenderar att ni minimerar närhet vid det fysiska mötet, och i första hand sköter betalning över exempelvis Swish. Då många äldre inte använder internettjänster kan det vara bra att vara förberedd på att få betalt i kontanter. Vi rekommenderar även att du sparar eventuella kvitton. Gör upp om detta innan du spenderar några pengar å den andres vägnar!"]

        const questions = ["Hur fungerar det?",
                "Hur ska vi hantera betalningar och leveranser?",
                "Vad gör detta för att underlätta coronakrisen?",
                "Kan jag hjälpa mer än en pensionär?",
                "Hur drar jag mig ur rollen som volontär?",
                "Hur finansieras tjänsten?",
                "Kan jag lita på att ni hanterar min data på ett bra sätt?"
                ];

        const answers = ["När du skriver upp dig som volontär ber vi dig att uppge ditt tilltalsnamn, telefonnummer, och postnummer. När en hemmasittande person ringer upp Telehelp kommer de att själva uppge sitt postnummer, och kopplas därefter ihop med volontärer i närområdet. Om du blir uppringd kommer ni att få gemensamt bestämma hur ni vill hantera ärendet - Telehelp står bara för att etablera kontakten. Om du eller pensionären själv ringer upp det nummer du blivit uppringd ifrån, kommer ni automatiskt att bli ihopkopplade - på så vis måste ni inte skriva ner några telefonnummer till varandra.",
                "Telehelp bidrar endast med att knyta samman pensionärer och volontärer. Det är upp till er att gemensamt hitta en lösning som fungerar för båda parter. Vi rekommenderar att ni minimerar närhet vid det fysiska mötet, och i första hand sköter betalning över exempelvis Swish. Då många äldre inte använder internettjänster kan det vara bra att vara förberedd på att få betalt i kontanter. Vi rekommenderar även att du sparar eventuella kvitton. Gör upp om detta innan du spenderar några pengar å den andres vägnar!",
                "Enligt Folkhälsomyndigheten (se: https://omni.se/folkhalsomyndighetens-nya-rad-aldre-bor-undvika-mataffarer-helt-och-hallet/a/Vb8PjW) bör inte personer som tillhör riskgrupper besöka matvarubutiker om de kan undvika detta, för att minimera antalet hårt drabbade av viruset.",
                "För att minimera smittorisken och förenkla användarupplevelsen är tjänsten byggd för att du ska kunna paras ihop med en enda person i riskgruppen i taget. Pensionären kan när som helst välja att byta till en annan volontär, vartefter ni inte längre kan komma i kontakt. Även du själv kan ta bort ditt konto om du inte längre vill använda tjänsten, men vi rekommenderar att du förklarar detta för den du hjälper först.",
                "Om du känner dig helt säker på att du inte vill vara en vardagshjälte, så kan du antingen ringa upp numret själv och följa instruktionerna, eller maila oss för att vi ska ta bort ditt telefonnummer manuellt ur vår databas. Om du redan har kontakt med en pensionär rekommenderar vi att du förklarar varför du inte längre kan hjälpa till innan du gör detta.",
                "Detta projekt startades under Hack The Crisis, ett initiativ från svenska regeringen, lett av Myndigheten för Digital Förvaltning (DIGG). <se: www.hackthecrisis.se/ > Vi och våra sponsorer/tredjepartsverktyg (46elks, AWS, Google Cloud, Domainkiosk/nameisp, etc) står i dagsläget för alla driftskostnader, men vi kommer öppna för donationer vid behov. Hör gärna av dig på info@telehelp.se",
                "Vi har gjort vårt bästa för att hitta en lösning som kräver så lite personlig information om både personerna i riskgrupp och volontärer som möjligt: endast ett telefonnummer och en postkod. Ett tilltalsnamn används också för att göra tjänsten mer personlig. Den som använder tjänsten får aldrig reda på den andra personens telefonnummer, och kan när som helst avbryta möjligheten till kommunikation till och från den andra parten."
            ];
        
        const zipped = zip(questions, answers);

        return (
            <div className="faq" id="faq">
                <h2>Vanliga frågor</h2>
                {zipped.map((e, i) => {
                    return (
                        <span key={i}>
                            <UncontrolledCollapse key={i} toggler={"faq-toggle-"+i}>
                            </UncontrolledCollapse>
                            <Button key={i} color="info" id={"faq-toggle-"+i} style={{ marginBottom: '1rem', marginRight: '1rem' }}>
                                {e[0]}
                            </Button>
                            <UncontrolledCollapse key={i} toggler={"faq-toggle-"+i}>
                            <p>
                                {e[1]}
                            </p>
                            </UncontrolledCollapse>
                        </span>
                    )
                })}
                {/*
                    {questions.map((element, i) => {
                        return <Button key={i} color="info" id={"faq-toggle-"+i} style={{ marginBottom: '1rem', marginRight: '1rem' }}>
                            {element}
                        </Button>
                    })}
                   {answers.map((element, i) => {
                        return<UncontrolledCollapse key={i} toggler={"faq-toggle-"+i}>
                        <p>
                            {element}
                        </p>
                      </UncontrolledCollapse>
                    })}
                */}
            </div>
        )
    }
}
export default FAQ;
