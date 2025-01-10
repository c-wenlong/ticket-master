type Optional<T> = T | null;
type Result<T, E = string> = { ok: true; value: T } | { ok: false; error: E };
