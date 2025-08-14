import React from "react";
import "../styles/Features.css";

const FeaturesComponent = () => {
  return (
    <div>
      <h5>Features</h5>
      <table className="table table-hover table-bordered">
        <tbody>
          <tr>
            <td className="features">
              <th>Summarize Research Papers in seconds.</th>
              Upload any research paper in PDF format and get a concise summary
              of the paper in seconds. The summary is generated using fine-tuned
              T5 transformer, ensuring that you get the most relevant
              information without having to read through the entire paper.
            </td>
          </tr>
          <tr>
            <td className="features">
              <th>Question Answering powered by Llama2</th>
              Ask any question related to the research paper and get accurate
              answers in real-time. The question-answering system is powered by
              Llama2, a state-of-the-art language model that understands the
              context of the paper and provides precise answers.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default FeaturesComponent;
