// https://nextjs.org/docs/app/building-your-application/rendering/client-components
// Next.js has client and server components

"use client";

import { useEffect, useState } from "react";
import { Document } from "../../types/types";

export default function Documents() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    const documents = fetch("http://localhost:5000/documents")
      .then((response) => response.json())
      .then((data) => {
        setDocuments(data);
      });
  });

  const transformDate = (date: string) => {
    return new Date(date).toLocaleDateString();
  };

  return (
    <main>
      <h1>Documents</h1>
      {documents.map((document: Document) => (
        <div key={document.id}>
          <h2>Title: {document.title}</h2>
          <p>Body: {document.body}</p>
          <p>Published: {transformDate(document.published_date)}</p>
        </div>
      ))}
    </main>
  );
}
