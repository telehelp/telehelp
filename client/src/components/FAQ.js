import React from "react";
import { UncontrolledCollapse, Button } from "reactstrap";

class FAQ extends React.Component {
  render() {
    const entries = [
      {
        question: "How does it work?",
        answer: (
          <p>
            When you sign up as a volunteer, we ask you to provide a nickname,
            phone number, and postal code. When a self-isolating person calls
            Telehelp, they too will key in their postal code over the phone,
            which allows said person to be connect with local volunteers. If you
            get called up, you will have to clarify what the person needs help
            with and how to handle the logistics - Telehelp only provides a way
            of establishing contact. If you or the at-risk person call up the
            number again, you will automatically be connected - no need to write
            down any phone numbers!{" "}
            <a href="https://www.youtube.com/watch?v=4dXq6gTrPCQ">Here</a> is a
            link to a short informational video.
          </p>
        ),
      },
      {
        question: "How should we handle payments and delivery?",
        answer: (
          <p>
            Telehelp only provides a way to establish contact between at-risk
            groups and volunteers. It is up to the users to find a solution for
            the logistics. We recommend that you minimize close contact upon
            delivery, but for example leaving items by the door. Digital
            payments are preferred, but since many older citizens do not use
            internet services, you should be prepared to handle cash. We also
            recommend that you save any receipts to prove what the groceries
            cost, for example. Have a plan for how to handle this before
            spending money!
          </p>
        ),
      },
      {
        question: "How does this help during the COVID-19 crisis?",
        answer: (
          <p>
            According to the{" "}
            <a href="https://omni.se/folkhalsomyndighetens-nya-rad-aldre-bor-undvika-mataffarer-helt-och-hallet/a/Vb8PjW">
              Swedish Folkhälsomyndigheten
            </a>{" "}
            people who belong to at-risk groups should try to avoid grocery
            stores if possible to minimize the number of infected, who may
            potentially get lethally sick. Stay safe!
          </p>
        ),
      },
      {
        question: "Can I help more than one self-isolating person?",
        answer: (
          <p>
            To minimize the risk of infection, and simplify the user experience
            the Telehelp service is build to get paired up with one person at a
            time. The person asking for help can at any point choose to switch
            to another volunteer, after which the two of you can no longer get
            in touch. You, as a volunteer, can also remove your account if you
            no longer want to help out, but we strongly recommend that you reach
            out to your contact and explain this beforehand to avoid confusion.
          </p>
        ),
      },
      {
        question: "How can I stop being a volunteer?",
        answer: (
          <p>
            If you are sure that you no longer want to be an everyday hero, you
            can either call up the number yourself and follow the instructions,
            or send us an email to get manually removed from our database. If
            you already have a contact person, we strongly recommend that you
            reach out to your contact and explain this beforehand to avoid
            confusion.
          </p>
        ),
      },
      {
        question: "Who pays for it all?",
        answer: (
          <p>
            This project was created during{" "}
            <a href="https://hackthecrisis.se/">Hack The Crisis Sweden</a>, an
            initiative from the Swedish government. We and our sponsors (46elks,
            AWS, Google Cloud, Domainkiosk/nameisp, etc) currently cover all
            costs, but we will open for donations if necessary. Please get in
            touch at <a href="mailto:info@telehelp.se">info@telehelp.se</a>
          </p>
        ),
      },
      {
        question: "Can I trust that you handle my personal data correctly?",
        answer: (
          <p>
            We have done our best to find a solution that needs as little
            personal information about the users as possible: just a phone
            number and postal code. A nickname is also used to identify the
            volunteers to the person calling in repeatedly. The person calling
            in never gets access to the other person's phone number, and can at
            any point remove the possibility of getting called up by the other
            party or unregister from the service entirely.
          </p>
        ),
      },
    ];

    return (
      <div className="faq" id="faq">
        <h2>Frequently Asked Questions</h2>
        {entries.map((e, i) => {
          return (
            <div key={i}>
              <Button
                color="info"
                id={"faq-toggle-" + i}
                style={{ marginBottom: "1rem", marginRight: "1rem" }}
              >
                {e.question}
              </Button>
              <UncontrolledCollapse toggler={"faq-toggle-" + i}>
                {e.answer}
              </UncontrolledCollapse>
            </div>
          );
        })}
      </div>
    );
  }
}
export default FAQ;
