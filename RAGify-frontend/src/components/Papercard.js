import React from "react";
import { Card } from "react-bootstrap";

const PaperCard = ({ title, link }) => (
  <Card className="mb-3 w-100" style={{ maxWidth: 700 }}>
    <Card.Body>
      <Card.Title style={{ fontSize: "1.1rem" }}>{title}</Card.Title>
      <Card.Link href={link} target="_blank" rel="noopener noreferrer">
        Download PDF
      </Card.Link>
      <Card.Link
        href={`/view?title=${encodeURIComponent(
          title
        )}&link=${encodeURIComponent(link)}`}
      >
        Explore
      </Card.Link>
    </Card.Body>
  </Card>
);

export default PaperCard;
