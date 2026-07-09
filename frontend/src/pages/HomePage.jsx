// Home page for introducing the AIIP internship demo workflow.
import React from "react";
import { ArrowRight, BrainCircuit, FileText, GraduationCap, ListChecks } from "lucide-react";

const capabilities = [
  {
    icon: FileText,
    title: "PDF Text Extraction",
    text: "Upload an assignment PDF and extract readable academic text for review.",
  },
  {
    icon: BrainCircuit,
    title: "IBM Granite Analysis",
    text: "Send the extracted text to IBM Granite for a structured integrity report.",
  },
  {
    icon: ListChecks,
    title: "Actionable Report",
    text: "View summary, plagiarism observations, AI-writing signals, citations, and recommendations.",
  },
];

export default function HomePage({ onNavigate }) {
  return (
    <div className="space-y-8">
      <section className="grid gap-8 rounded-md bg-white p-7 shadow-soft lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 rounded-md bg-blue-50 px-3 py-2 text-sm font-semibold text-ibm">
            <GraduationCap size={18} />
            IBM AICTE Internship Demo
          </div>
          <div className="space-y-4">
            <h1 className="text-4xl font-bold tracking-normal text-ink md:text-5xl">
              Academic Integrity Intelligence Platform
            </h1>
            <p className="max-w-2xl text-lg leading-8 text-slate-600">
              A clean full-stack demo that reviews assignment PDFs, extracts text, and generates
              an academic integrity report using IBM Granite.
            </p>
          </div>
          <button
            className="inline-flex h-12 items-center gap-2 rounded-md bg-ibm px-5 font-semibold text-white transition hover:bg-blue-700"
            onClick={() => onNavigate("upload")}
            type="button"
          >
            Start PDF Review
            <ArrowRight size={18} />
          </button>
        </div>

        <div className="rounded-md border border-slate-200 bg-slate-50 p-5">
          <div className="space-y-4">
            {["Upload assignment PDF", "Extract PDF text", "Analyze with IBM Granite", "Display report"].map(
              (step, index) => (
                <div key={step} className="flex items-center gap-4 rounded-md bg-white p-4">
                  <span className="flex h-9 w-9 items-center justify-center rounded-md bg-blue-100 font-bold text-ibm">
                    {index + 1}
                  </span>
                  <span className="font-semibold text-slate-800">{step}</span>
                </div>
              ),
            )}
          </div>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {capabilities.map((item) => {
          const Icon = item.icon;
          return (
            <article key={item.title} className="rounded-md border border-slate-200 bg-white p-5">
              <Icon className="mb-4 text-ibm" size={28} />
              <h2 className="mb-2 text-lg font-bold">{item.title}</h2>
              <p className="leading-7 text-slate-600">{item.text}</p>
            </article>
          );
        })}
      </section>
    </div>
  );
}
