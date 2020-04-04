import React from 'react';
import { useForm } from 'react-hook-form';

function RegistrationForm() {
  const { register, handleSubmit, errors } = useForm(); // initialise the hook
  const onSubmit = data => {
    console.log(data);
    
    fetch('/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="display-flex">
        <div className="block">
        <label> Name
        <input name="firstname" ref={register({ required: true })} />
        </label>
        {errors.firstname && '(Please enter your name.)'}
        </div>

        <div className="block">
        <label> Zip code
        <input name="zipcode" ref={register({ pattern: /\d+/, required: true })} />
        </label>
        {errors.zipcode && '(Please enter your zipcode.)'}
        </div>

        <div className="block">
        <label> Phone number
        <input name="phonenumber" ref={register({ pattern: /\d+/, required: true })} />
        </label>
        {errors.zipcode && '(Please enter a valid phone number.)'}

        </div>
        <div className="block">
        <label>
        <input type="checkbox" name="terms" ref={register({required: true})} />
        I accept the terms and conditions 
        </label>
        {errors.zipcode && '(You must accept the terms and conditions)'}
        </div>
        <div className="block">
        <input type="submit" value="Sign up"/>
        </div>
    </form>
  );
}

export default RegistrationForm;