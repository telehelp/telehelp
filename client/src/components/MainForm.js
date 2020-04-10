import React from "react";
import VerificationForm from "./VerificationForm";
import CompleteForm from "./CompleteForm";
import RegistrationForm from "./RegistrationForm";
import { useSelector } from "react-redux";
import { FormStatus } from "../actions";

function MainForm() {
  const progress = useSelector((state) => state.registration.progress);

  let form;

  switch (progress) {
    case FormStatus.CANNOT_CONNECT:
      form = (
        <CompleteForm
          message={
            "Kan inte kommunicera med servern! Försök gärna igen lite senare."
          }
        />
      );
      break;
    case FormStatus.REGISTRATION_COMPLETE:
      form = <CompleteForm message={"Tack för din registrering!"} />;
      break;
    case FormStatus.VERIFICATION_FAILED:
      form = <CompleteForm message={"Verifiering misslyckades!"} />;
      break;
    case FormStatus.VERIFY_NUMBER:
      form = <VerificationForm />;
      break;
    case FormStatus.BAD_DETAILS:
      form = (
        <CompleteForm
          message={
            "Kunde inte genomföra registrering, du kanske redan har registrerat dig?"
          }
        />
      );
      break;
    case FormStatus.REGISTER_DETAILS:
    default:
      form = <RegistrationForm />;
      break;
  }

  return (
    <div className="signup" id="register">
      {form}
    </div>
  );
}

export default MainForm;
