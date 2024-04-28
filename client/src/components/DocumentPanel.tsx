import { useState } from "react";
import { Document } from "../types/types";

const DocumentPanel = ({
  document,
  rerenderParent,
  updateDocument,
}: {
  document: Document;
  rerenderParent: () => void;
  updateDocument: (document: Document) => void;
}) => {
  const [publishedDateToggle, setPublishedDateToggle] =
    useState<boolean>(false);

  const transformDate = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  const [date, setDate] = useState<string>(
    transformDate(document.published_date)
  );

  const togglePublishedDate = () => {
    setPublishedDateToggle(!publishedDateToggle);
  };

  const submitPublishedDate = () => {
    // Update current document in the database
    // fetch(`http://localhost:5000/documents/${document.id}`, {
    //   method: "PUT",
    //   body: JSON.stringify({ published_date: date }),
    // });
    // Then cause a re-render for parent component
    // rerenderParent();
    // Or, knowing the database update succeeded
    // We just update the array in parent component
    // updateDocument(document);
  };

  const PublishedDate = (document: Document) => {
    if (publishedDateToggle) {
      return (
        <div style={{ display: "inline-block" }}>
          <input value={date}></input>
          <button
            onClick={() => {
              submitPublishedDate();
              togglePublishedDate();
            }}
          >
            Submit
          </button>
        </div>
      );
    } else {
      return (
        <div style={{ display: "inline-block" }}>
          {`Published: ${transformDate(document.published_date)} `}
          <button onClick={togglePublishedDate}>Edit</button>
        </div>
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
