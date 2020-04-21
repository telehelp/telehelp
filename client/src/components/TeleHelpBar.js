import React, { useState } from "react";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavItem,
  NavLink,
} from "reactstrap";
import { Link } from "react-router-dom";

const TeleHelpBar = (props) => {
  const [collapsed, setCollapsed] = useState(true);

  const toggleNavbar = () => setCollapsed(!collapsed);

  return (
    <div>
      <div class="container">
        <Navbar color="faded" light className="telebar navbar-expand-lg">
          <NavbarBrand href="/" className="mr-auto">
            <img
              src="img/logo/telehelp-logo-heart.svg"
              alt="telehelp"
              height="50px"
            />
          </NavbarBrand>
          <NavbarToggler onClick={toggleNavbar} />
          <Collapse isOpen={!collapsed} navbar className="ml-auto">
            {/*             <Nav navbar className="nav mx-auto">
              <NavItem className="tele-number">
                <NavLink href="tel:+46766861551">
                  <i className="fas fa-mobile icon-before"></i>
                  076-686 15 51
                </NavLink>
              </NavItem>
            </Nav> */}
            <Nav navbar className="nav ml-auto">
              <NavItem>
                <NavLink href="/#faq">Frågor & Svar</NavLink>
              </NavItem>
              <NavItem>
                <Link to="/about" style={{ textDecoration: "none" }}>
                  <NavLink>Om oss</NavLink>
                </Link>
              </NavItem>
            </Nav>
          </Collapse>
        </Navbar>
      </div>
    </div>
  );
};

export default TeleHelpBar;
