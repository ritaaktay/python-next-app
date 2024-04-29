import { useState } from "react";
import { Document } from "../types/types";
import { api } from "@/constants/api";

export const PublishedDate = ({
  document,
  updateDocument,
}: // renderParent,
{
  document: Document;
  updateDocument: (document: Document) => void;
  // renderParent?: () => void;
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
      const res = await fetch(`${api}/documents/${document.id}`, {
        method: "PUT",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          published_date: date,
        }),
      });
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
            onClick={async () => {
              await submitPublishedDate();
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
