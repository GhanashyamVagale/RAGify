import React from "react";
import { Form, Button, Spinner } from "react-bootstrap";

const SearchForm = ({ title, setTitle, handleSearch, loading }) => (
  <Form onSubmit={handleSearch} className="w-100" style={{ maxWidth: 500 }}>
    <Form.Control
      type="text"
      placeholder="Enter paper title or topic"
      value={title}
      onChange={(e) => setTitle(e.target.value)}
    />
    <Button
      variant="primary"
      type="submit"
      className="mt-3 w-100"
      disabled={loading}
    >
      {loading ? <Spinner animation="border" size="sm" /> : "Search Papers"}
    </Button>
  </Form>
);

export default SearchForm;
