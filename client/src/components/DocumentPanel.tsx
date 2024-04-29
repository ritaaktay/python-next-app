import { Document } from "../types/types";
import { PublishedDate } from "./PublishedDate";
import { Author } from "./Author";

const DocumentPanel = ({
  document,
  // rerenderParent,
  updateDocument,
}: {
  document: Document;
  // rerenderParent: () => void;
  updateDocument: (document: Document) => void;
}) => {
  return (
    <div key={document.id} style={{ display: "flex", flexDirection: "column" }}>
      <h2>Title: {document.title}</h2>
      <p>Body: {document.body}</p>
      <PublishedDate document={document} updateDocument={updateDocument} />
      <br></br>
      <Author document={document} updateDocument={updateDocument} />
    </div>
  );
};

export default DocumentPanel;
