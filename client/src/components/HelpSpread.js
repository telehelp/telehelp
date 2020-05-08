import React from "react";

const HelpSpread = () => {
  return (
    <div className="introduction">
      <h2>Hjälp oss att nå riskgrupper</h2>
      <p>Hjälp oss att berätta om telehelp, till de som behöver hjälp.</p>
      <p>
        <ol className="cta-list">
          <li>Sprid numret 076-686 15 51</li>
          <li>
            Skriv ut{" "}
            <a
              href="/static/flyer.pdf"
              target="_blank"
              rel="noopener noreferrer"
            >
              detta informationsblad
            </a>{" "}
            och sätt upp i din trappuppgång, i din på din lokala butik eller på
            andra ställen där du tror att riskgrupper kan se den.
          </li>
        </ol>
      </p>
    </div>
  );
};

export default HelpSpread;
