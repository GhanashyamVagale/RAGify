import React from "react";
import { Navbar, NavbarBrand } from "react-bootstrap";
import "../App.css";

const NavbarComponent = () => {
  return (
    <Navbar bg="dark" variant="dark">
      <NavbarBrand href="/" className="mx-4">
        {/* <img src="./jobsage_logo.jpg" className="logo mx-2"></img> */}
        RAGnify
      </NavbarBrand>
      <NavbarBrand href="/connect" className="fs-6 mx-10">
        Connect
      </NavbarBrand>
    </Navbar>
  );
};

export default NavbarComponent;
