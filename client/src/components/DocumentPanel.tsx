import { Document } from "../types/types";
import { PublishedDate } from "./PublishedDate";

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
    <div key={document.id}>
      <h2>Title: {document.title}</h2>
      <p>Body: {document.body}</p>
      <PublishedDate document={document} updateDocument={updateDocument} />
    </div>
  );
};

export default DocumentPanel;
