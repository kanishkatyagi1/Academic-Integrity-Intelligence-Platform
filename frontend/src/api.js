// Small API client for communicating with the FastAPI backend.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function uploadAssignment(file) {
  // Send a PDF file to the backend and receive extracted text.
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  return parseResponse(response);
}

export async function analyzeAssignment({ fileId, text }) {
  // Ask the backend to analyze extracted text with IBM Granite.
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ file_id: fileId, text }),
  });

  return parseResponse(response);
}

async function parseResponse(response) {
  // Convert fetch responses into JSON or throw a readable error.
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "The request could not be completed.");
  }
  return data;
}
