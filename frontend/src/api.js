export async function apiGet(path) {
  // Centralized GET helper keeps fetch/error behavior consistent across components.
  const res = await fetch(path);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

export async function apiPost(path, payload = {}) {
  // JSON POST helper used by move/command actions.
  const res = await fetch(path, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    // Surface HTTP status so callers can map it to UI alerts.
    throw new Error(`Request failed: ${res.status}`);
  }

  return res.json();
}
