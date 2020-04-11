import React from "react";

const BackgroundInfo = () => {
  return (
    <div className="introduction">
      <h2>Help your neighbors handle daily chores!</h2>
      <p>
        If you belong to an at-risk group, or are currently infected by the
        coronavirus, you can call Telehelp's phone number to quickly get in
        touch with a local volunteer who can help you out.
      </p>
      <div className="row">
        <div className="col-md-12 text-center">
          <img
            className="img-fluid"
            src="/img/old-people.png"
            alt="Two happy old people on a bench"
          ></img>
        </div>
      </div>
      <p>
        By registering as a volunteer, local people in need of assistance during
        the COVID-19 crisis can get in touch. Examples of tasks that may be
        unsafe for these people to do normally during these times include
        shopping for groceries or picking up medicine at the pharmacy. Telehelp
        especially focuses on being accessible to anyone, even those without
        access to the internet.
      </p>
    </div>
  );
};

export default BackgroundInfo;
