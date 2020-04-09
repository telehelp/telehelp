import React from 'react';
import { useForm } from 'react-hook-form';
import { Form, FormFeedback, Label, FormGroup, Input, Button } from 'reactstrap';
import { setRegistrationProgress, FormStatus } from '../actions';
import { useDispatch, useSelector} from 'react-redux';

function VerificationForm() {
  const dispatch = useDispatch();
  const phoneNumber = useSelector(state => state.registration.number);

  const { register, handleSubmit, errors, reset } = useForm(); // initialise the hook
  const onSubmit = data => {
    console.log(data);
    if (!data)
    {
        console.log("Failed submitting, reason: no data")
        return;
    }

    console.log(phoneNumber)

    const newData = Object.assign({}, data, {
      number: phoneNumber
    });

    fetch('/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newData)
    })
    .then(res => res.json())
    .then(respData => {
      // Not sure if redux allows this, should probably be done in a reducer
      if (respData.type === "success")
      {
        dispatch(setRegistrationProgress(FormStatus.REGISTRATION_COMPLETE));
      }
      else
      {
        dispatch(setRegistrationProgress(FormStatus.VERIFICATION_FAILED));
      }
    });
  };

  //if progress ngt
  //use a main form to do this
  // The main form should have all three steps
  const message = "Skriv in koden som vi skickade dig"

  return (
    <Form onSubmit={handleSubmit(onSubmit)} >
     <h4>{message}</h4>
     <FormGroup>
      <Label for="Verifieringskod">Verifieringkod</Label>
        <Input
          name="verificationCode"
          id="verificationCode"
          placeholder="123456"
          invalid={'verificationCode' in errors}
          innerRef={register({pattern: /^[0-9]{6}$/, required: true })}/>
        <FormFeedback invalid>Skriv in en sexsiffrig kod</FormFeedback>
      </FormGroup>
      <Button color="info">Registrera</Button>
    </Form>
  );
}

export default VerificationForm;
