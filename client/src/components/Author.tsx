import { useState } from "react";
import { Document } from "../types/types";

export const Author = ({
  document,
  updateDocument,
}: {
  document: Document;
  updateDocument: (document: Document) => void;
}) => {
  const [editToggle, setEditToggle] = useState<boolean>(false);

  const [error, setError] = useState<string>("");

  const [authorName, setAuthorName] = useState<string>(document.author.name);

  const toggleEdit = () => {
    setEditToggle(!editToggle);
  };

  const submitAuthor = async () => {
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
            author: {
              name: authorName,
            },
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

  if (editToggle) {
    return (
      <div style={{ display: "inline-block" }}>
        <input
          onChange={(e) => setAuthorName(e.target.value)}
          value={authorName}
        ></input>
        <button
          onClick={async () => {
            await submitAuthor();
            toggleEdit();
          }}
        >
          Submit
        </button>
      </div>
    );
  } else {
    return (
      <>
        <div style={{ display: "inline-block" }}>
          {`Author: ${document.author.name} `}
          <button onClick={toggleEdit}>Edit</button>
        </div>
        {error ? <p style={{ color: "red" }}>{error}</p> : null}
      </>
    );
  }
};
