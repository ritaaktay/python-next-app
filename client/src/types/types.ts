export interface Author {
  name: string;
  id: number;
}

export interface Document {
  title: string;
  body: string;
  published_date: string;
  id: number;
  author: Author;
  author_id: number;
}
