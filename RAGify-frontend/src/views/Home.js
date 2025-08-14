import React, { useState } from "react";
import "../App.css";
import { Container } from "react-bootstrap";
import axios from "axios";
import NavbarComponent from "../components/Navbar";
import FeaturesComponent from "../components/Features";
import SearchForm from "../components/Searchform";
import PaperCard from "../components/Papercard";

const HomePage = () => {
  const [title, setTitle] = useState("");
  const [papers, setPapers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPapers([]);
    setError("");

    console.log(title);
    try {
      const response = await axios.post(
        "http://localhost:4000/search_papers/",
        {
          title: title,
        }
      );

      setPapers(response.data.papers || []);
    } catch (err) {
      console.error(err);
      setError("Failed to fetch papers. Please try again.");
    } finally {
      setLoading(false);
    }
    setTitle("");
  };

  return (
    <div>
      <NavbarComponent />
      <div className="mx-4 my-4">
        <Container align="center">
          <h3>RAGnify: RAG-Based Intelligent Research Assistant for Summarization and QA</h3>
        </Container>
        <div className="my-4">
          <FeaturesComponent />
        </div>
        <div className="my-4">
          <SearchForm
            title={title}
            setTitle={setTitle}
            handleSearch={handleSearch}
            loading={loading}
          />
        </div>
        <div className="my-4">
          {papers.length > 0 && (
            <div className="mt-5 w-100 d-flex flex-column align-items-center">
              <h5 className="mb-3">Results:</h5>
              {papers.map((paper, idx) => (
                <PaperCard key={idx} title={paper.title} link={paper.link} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;
