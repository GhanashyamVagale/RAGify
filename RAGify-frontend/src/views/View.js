import React, { useState, useEffect } from "react";
import "../App.css";
import { Container, Card, Spinner, Form, Button } from "react-bootstrap";
import axios from "axios";
import { useLocation } from "react-router-dom";
import NavbarComponent from "../components/Navbar";

const ViewPage = () => {
  const query = new URLSearchParams(useLocation().search);
  // const title = query.get("title");
  const link = query.get("link");
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [qloading, setQloading] = useState(false);

  useEffect(() => {
    uploadPaper();
    fetchSummary();
  }, []);

  const fetchSummary = async () => {
    setLoading(true);
    setSummary("");

    try {
      const response = await axios.post(
        "http://localhost:3001/summarize_paper/",
        {
          url: link,
        }
      );

      setSummary(response.data.summary || "");
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const uploadPaper = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/store_to_pinecone/",
        {
          url: link,
        }
      );
      console.log(response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setQloading(true);
    setAnswer("");

    try {
      const response = await axios.post(
        "http://localhost:8000/query_pinecone/",
        {
          query: question,
        }
      );

      setAnswer(response.data.answer || "");

      console.log(answer);
    } catch (error) {
      console.error("Error submitting form:", error);
      alert("Failed to submit form. Please try again.");
    } finally {
      setQloading(false);
    }
  };

  return (
    <div>
      <NavbarComponent />
      <Container className="mt-5">
        <h3>Paper Summary</h3>
        {loading ? (
          <Spinner animation="border" />
        ) : (
          <Card
            className="mt-3"
            style={{
              backgroundColor: "#36454F",
              border: "1px solid white",
              color: "white",
              borderRadius: "0.25rem",
            }}
          >
            <Card.Body>
              <Card.Text>{summary}</Card.Text>
            </Card.Body>
          </Card>
        )}
      </Container>
      <Container className="mt-5">
        <h3>QA</h3>
        <Form onSubmit={handleSubmit}>
          <Form.Group controlId="formQuestion">
            <Form.Label>Question</Form.Label>
            <Form.Control
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="form"
            />
          </Form.Group>
          <Button
            variant="secondary"
            type="submit"
            className="mt-3"
            disabled={loading}
          >
            {qloading ? <Spinner animation="border" size="sm" /> : "Submit"}
          </Button>
        </Form>
        {answer && (
          <div>
            <h3>Answer</h3>
            <Card
              className="mt-2"
              style={{
                backgroundColor: "#36454F",
                border: "1px solid white",
                color: "white",
              }}
            >
              <Card.Body>
                <Card.Text>{answer}</Card.Text>
              </Card.Body>
            </Card>
          </div>
        )}
      </Container>
    </div>
  );
};

export default ViewPage;
