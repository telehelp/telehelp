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
          message={"Could not communicate with the server. Try again later."}
        />
      );
      break;
    case FormStatus.REGISTRATION_COMPLETE:
      form = <CompleteForm message={"Thanks for your solidarity!"} />;
      break;
    case FormStatus.VERIFICATION_FAILED:
      form = <CompleteForm message={"Verification failed!"} />;
      break;
    case FormStatus.VERIFY_NUMBER:
      form = <VerificationForm />;
      break;
    case FormStatus.BAD_DETAILS:
      form = (
        <CompleteForm
          message={
            "The registration could not be completed, maybe you are already registered?"
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
