// https://nextjs.org/docs/app/building-your-application/rendering/client-components
// Next.js has client and server components

"use client";

import { useEffect, useState } from "react";
import { Document } from "../../types/types";
import DocumentPanel from "../../components/DocumentPanel";
import { api } from "@/constants/api";

export default function Page() {
  const [documents, setDocuments] = useState<Document[]>([]);
  //   const [rerender, setRerender] = useState<boolean>(false);

  useEffect(() => {
    const res = fetch(`${api}/documents`)
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setDocuments(data.sort((a: Document, b: Document) => a.id - b.id));
      });
  }, []);
  //   }, [rerender]);

  //   const forceRerender = () => {
  //     setRerender(!rerender);
  //   };

  const updateDocument = (document: Document) => {
    const newDocuments = documents.map((doc) => {
      if (doc.id === document.id) {
        return document;
      }
      return doc;
    });
    setDocuments(newDocuments);
  };

  return (
    <main>
      <h1>Documents</h1>
      {documents.map((document: Document) => (
        <div key={document.id}>
          <DocumentPanel
            document={document}
            // rerenderParent={forceRerender}
            updateDocument={updateDocument}
          />
        </div>
      ))}
    </main>
  );
}
