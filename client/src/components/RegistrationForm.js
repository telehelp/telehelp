import React from 'react';
import { useForm } from 'react-hook-form';
import { Form, FormFeedback, FormGroup, Label, Input, Button } from 'reactstrap';

function RegistrationForm() {
  const { register, handleSubmit, errors, reset } = useForm(); // initialise the hook
  const onSubmit = data => {
    console.log(data);
    if (!data)
    {
        console.log("Failed submitting, reason: no data")
        return;
    }
    fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    reset();
  };

  return (
    <Form onSubmit={handleSubmit(onSubmit)} >
    <h4>Registrera dig som volontär!</h4>
    <FormGroup>
        <Label for="helperName">Tilltalsnamn</Label>
        <Input 
            name="helperName"
            id="helperName"
            placeholder="Bengan"
            invalid={'helperName' in errors}
            innerRef={register({ required: true })}/>
        <FormFeedback invalid></FormFeedback>
    </FormGroup>
     <FormGroup>
     <Label for="zipCode">Postnummer</Label>
        <Input 
            name="zipCode"
            id="zipCode"
            placeholder="12345"
            invalid={'zipCode' in errors}
            innerRef={register({pattern: /\d+/, required: true })}/>
        <FormFeedback invalid>Den postnummer som du skrev in är ogilitigt</FormFeedback>
      </FormGroup>
      <FormGroup>
     <Label for="phoneNumber">Telefonnummer</Label>
        <Input 
            name="phoneNumber"
            id="phoneNumber"
            placeholder="0701234567"
            invalid={'phoneNumber' in errors}
            innerRef={register({pattern: /\d+/, required: true })}/>
        <FormFeedback invalid>Det telefonnummer som du skrev in är ogilitigt</FormFeedback>
      </FormGroup>
      <FormGroup>
      <Input 
            type="checkbox"
            name="terms"
            id="terms"
            invalid={'terms' in errors}
            innerRef={register({required: true })}/>
        <Label for="terms">Jag accepterar <a href="/terms-and-conditions.pdf">användarvillkoren</a></Label>
        <FormFeedback invalid>Du måste acceptera användarvillkoren</FormFeedback>
      </FormGroup>
      <Button color="info">Registrera</Button>
    </Form>
  );
}

export default RegistrationForm;