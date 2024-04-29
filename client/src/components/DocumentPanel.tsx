import { useState } from "react";
import { Document } from "../types/types";

const DocumentPanel = ({
  document,
  // rerenderParent,
  updateDocument,
}: {
  document: Document;
  // rerenderParent: () => void;
  updateDocument: (document: Document) => void;
}) => {
  const [publishedDateToggle, setPublishedDateToggle] =
    useState<boolean>(false);

  const [error, setError] = useState<string>("");

  const transformDateDisplay = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  const [date, setDate] = useState<string>(document.published_date);

  const togglePublishedDate = () => {
    setPublishedDateToggle(!publishedDateToggle);
  };

  const submitPublishedDate = async () => {
    try {
      const res = await fetch(
        `http://localhost:5000/documents/${document.id}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            published_date: date,
          }),
        }
      );
      if (res.ok) {
        const data = await res.json();
        // Update the array in parent component
        updateDocument(data);
        // Can also cause a re-render for parent component to fetch new data
        // rerenderParent();
      } else {
        throw new Error(res.statusText);
      }
    } catch (e) {
      setError("Error updating document, please try again");
      console.log("Error updating document", e);
    }
  };

  const PublishedDate = (document: Document) => {
    if (publishedDateToggle) {
      return (
        <>
          <div style={{ display: "inline-block" }}>
            <input
              type="date"
              onChange={(e) => setDate(e.target.value)}
              value={date}
            ></input>
            <button
              onClick={() => {
                submitPublishedDate();
                togglePublishedDate();
              }}
            >
              Submit
            </button>
          </div>
        </>
      );
    } else {
      return (
        <>
          <div style={{ display: "inline-block" }}>
            {`Published: ${transformDateDisplay(document.published_date)} `}
            <button onClick={togglePublishedDate}>Edit</button>
          </div>
          {error ? <p style={{ color: "red" }}>{error}</p> : null}
        </>
      );
    }
  };

  return (
    <div key={document.id}>
      <h2>Title: {document.title}</h2>
      <p>Body: {document.body}</p>
      {PublishedDate(document)}
    </div>
  );
};

export default DocumentPanel;
