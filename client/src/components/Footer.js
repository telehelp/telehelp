import React from "react";

const Footer = () => {
  return (
    <footer className="footer-copyright text-center tele-footer">
      <div className="container">
        <div className="row">
          <div className="col-lg-12 text-center">
            <p>© Telehelp 2020. Skapad under Hack the Crisis.</p>
            <p>
              Kontakt: <a href="mailto:info@telehelp.se">info@telehelp.se</a>
            </p>
            <a href="/static/terms-and-conditions.pdf" target="_blank">
              Användarvillkor
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
