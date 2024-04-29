import { useState } from "react";
import { Document } from "../types/types";
import { api } from "@/constants/api";

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
    console.log("DOCUMENT ID IS", document);
    try {
      const res = await fetch(`${api}/documents/${document.id}`, {
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
      });
      if (res.ok) {
        const data = await res.json();
        // Update the array in parent component
        console.log(res);
        updateDocument(data);
        // Can also cause a re-render for parent component to fetch new data
        // rerenderParent();
      } else {
        throw new Error(res.statusText);
      }
    } catch (e) {
      setError("Error updating author, please try again");
      console.log("Error updating author", e);
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
