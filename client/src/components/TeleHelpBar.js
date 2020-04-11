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
    <div className="row telebar">
      <div className="col-md-12">
        <Navbar color="faded" light>
          <NavbarBrand href="/" className="mr-auto">
            <img src="img/telehelp-logo.svg" alt="telehelp logo" />
          </NavbarBrand>
          <NavbarToggler onClick={toggleNavbar} className="mr-2" />
          <Collapse isOpen={!collapsed} navbar>
            <Nav navbar>
              <NavItem>
                <NavLink href="/#register">Register as a volunteer</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/#faq">Frequently asked questions</NavLink>
              </NavItem>
              <NavItem>
                <NavLink href="/static/terms-and-conditions.pdf">
                  Terms of Service
                </NavLink>
              </NavItem>
              <NavItem>
                <Link to="/about" style={{ textDecoration: "none" }}>
                  <NavLink>About us</NavLink>
                </Link>
              </NavItem>
              <NavItem>
                <Link to="/press" style={{ textDecoration: "none" }}>
                  <NavLink>In media</NavLink>
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
