// Upload page that performs PDF upload, extraction, and analysis.
import React from "react";
import { useState } from "react";
import { AlertCircle, CheckCircle2, FileText, Loader2, UploadCloud } from "lucide-react";
import { analyzeAssignment, uploadAssignment } from "../api.js";

export default function UploadPage({ onReportReady }) {
  // Track the selected PDF, extracted text, and request state.
  const [file, setFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState("");
  const [loadingStep, setLoadingStep] = useState("");

  async function handleSubmit(event) {
    // Run the full PDF review flow from one button.
    event.preventDefault();
    setError("");
    setUploadResult(null);

    if (!file) {
      setError("Choose a PDF assignment before starting the review.");
      return;
    }

    try {
      setLoadingStep("Extracting PDF text");
      const uploaded = await uploadAssignment(file);
      setUploadResult(uploaded);

      setLoadingStep("Analyzing with IBM Granite");
      const analyzed = await analyzeAssignment({
        fileId: uploaded.file_id,
        text: uploaded.text,
      });

      onReportReady({ upload: uploaded, analysis: analyzed });
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoadingStep("");
    }
  }

  const isLoading = Boolean(loadingStep);

  return (
    <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr]">
      <section className="rounded-md bg-white p-6 shadow-soft">
        <h1 className="mb-2 text-2xl font-bold">Upload Assignment PDF</h1>
        <p className="mb-6 leading-7 text-slate-600">
          Select a readable PDF. The backend will extract text first, then request an academic
          integrity report.
        </p>

        <form className="space-y-5" onSubmit={handleSubmit}>
          <label className="flex min-h-56 cursor-pointer flex-col items-center justify-center rounded-md border-2 border-dashed border-slate-300 bg-slate-50 p-6 text-center transition hover:border-ibm">
            <UploadCloud className="mb-3 text-ibm" size={34} />
            <span className="font-bold">{file ? file.name : "Choose PDF file"}</span>
            <span className="mt-2 text-sm text-slate-500">Only .pdf files are accepted</span>
            <input
              accept="application/pdf"
              className="sr-only"
              onChange={(event) => setFile(event.target.files?.[0] || null)}
              type="file"
            />
          </label>

          <button
            className="flex h-12 w-full items-center justify-center gap-2 rounded-md bg-ibm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-400"
            disabled={isLoading}
            type="submit"
          >
            {isLoading ? <Loader2 className="animate-spin" size={18} /> : <FileText size={18} />}
            {isLoading ? loadingStep : "Generate Integrity Report"}
          </button>
        </form>

        {error && (
          <div className="mt-5 flex gap-3 rounded-md border border-red-200 bg-red-50 p-4 text-red-700">
            <AlertCircle size={20} />
            <p>{error}</p>
          </div>
        )}
      </section>

      <section className="rounded-md border border-slate-200 bg-white p-6">
        <div className="mb-4 flex items-center justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold">Extracted Text Preview</h2>
            <p className="text-sm text-slate-500">Preview appears after upload extraction.</p>
          </div>
          {uploadResult && (
            <span className="inline-flex items-center gap-2 rounded-md bg-green-50 px-3 py-2 text-sm font-semibold text-green-700">
              <CheckCircle2 size={16} />
              {uploadResult.text_length} chars
            </span>
          )}
        </div>

        <div className="min-h-96 rounded-md bg-slate-950 p-4 font-mono text-sm leading-6 text-slate-100">
          {uploadResult?.text ? (
            <pre className="whitespace-pre-wrap">{uploadResult.text.slice(0, 4500)}</pre>
          ) : (
            <p className="text-slate-400">
              The extracted assignment text will appear here before it is sent for analysis.
            </p>
          )}
        </div>
      </section>
    </div>
  );
}
