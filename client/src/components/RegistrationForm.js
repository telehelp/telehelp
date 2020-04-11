import React from "react";
import { useForm } from "react-hook-form";
import {
  Form,
  FormFeedback,
  FormGroup,
  Label,
  Input,
  Button,
} from "reactstrap";
import {
  setRegistrationProgress,
  FormStatus,
  setPhoneNumber,
} from "../actions";
import { useDispatch } from "react-redux";
import { batchActions } from "redux-batched-actions";

function RegistrationForm(props) {
  const dispatch = useDispatch();

  const { register, handleSubmit, errors } = useForm();
  const onSubmit = (data) => {
    console.log(data);
    if (!data) {
      console.log("Failed submitting, reason: no data");
      return;
    }
    fetch("/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => {
        if (res.ok) {
          return res.json();
        }
        dispatch(setRegistrationProgress(FormStatus.CANNOT_CONNECT));
        return Promise.reject("No response from server");
      })
      .then((respData) => {
        if (respData.type === "success") {
          //Same here i am not sure redux allows this
          dispatch(
            batchActions([
              setRegistrationProgress(FormStatus.VERIFY_NUMBER),
              setPhoneNumber(data.phoneNumber),
            ])
          );
        } else {
          console.log("Bad details");
          dispatch(setRegistrationProgress(FormStatus.BAD_DETAILS));
        }
      });
  };

  //if progress ngt
  //use a main form to do this
  // The main form should have all three steps
  const message = "Register as a volunteer!";

  return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <h4>{message}</h4>
      <FormGroup>
        <Label for="helperName">Tilltalsnamn</Label>
        <Input
          name="helperName"
          id="helperName"
          placeholder="Johnny"
          invalid={"helperName" in errors}
          innerRef={register({ pattern: /^[a-z ,.'-]+$/i, required: true })}
        />
        <FormFeedback invalid>Skriv in ett ordentligt namn</FormFeedback>
      </FormGroup>
      <FormGroup>
        <Label for="zipCode">Postnummer</Label>
        <Input
          name="zipCode"
          id="zipCode"
          placeholder="12345"
          invalid={"zipCode" in errors}
          innerRef={register({ pattern: /^[0-9]{5}$/, required: true })}
        />
        <FormFeedback invalid>
          Det postnummer som du skrev in är ogilitigt, måste vara 5 siffror
        </FormFeedback>
      </FormGroup>
      <FormGroup>
        <Label for="phoneNumber">Telefonnummer</Label>
        <Input
          name="phoneNumber"
          id="phoneNumber"
          placeholder="0701234567"
          invalid={"phoneNumber" in errors}
          innerRef={register({
            pattern: /^[0]{1}\d{7,9}$|^[\+46]{3}\d{9}$/,
            required: true,
          })}
        />
        <FormFeedback invalid>
          The phone number you entered is invalid.
        </FormFeedback>
      </FormGroup>
      <FormGroup>
        <Input
          type="checkbox"
          name="terms"
          id="terms"
          invalid={"terms" in errors}
          innerRef={register({ required: true })}
        />
        <Label for="terms">
          I accept{" "}
          <a href="/static/terms-and-conditions.pdf">Terms of Service</a>
        </Label>
        <FormFeedback invalid>
          You must accept the Terms of Service
        </FormFeedback>
      </FormGroup>
      <Button color="info">Sign up</Button>
    </Form>
  );
}

export default RegistrationForm;
