export type Timestamped<T> = T & {
  created_at: string;
  updated_at: string;
};