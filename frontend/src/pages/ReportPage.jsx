// Report page that renders the generated academic integrity analysis.
import React from "react";
import { AlertTriangle, BadgeCheck, Brain, ClipboardList, FileQuestion, Lightbulb } from "lucide-react";

const sections = [
  { key: "plagiarism_observations", title: "Possible Plagiarism Observations", icon: FileQuestion },
  { key: "ai_generated_content", title: "Possible AI-Generated Content", icon: Brain },
  { key: "citation_suggestions", title: "Citation Suggestions", icon: ClipboardList },
  { key: "recommendations", title: "Recommendations", icon: Lightbulb },
];

export default function ReportPage({ analysis, onNavigate }) {
  // Show a helpful empty state when no report has been created yet.
  if (!analysis?.analysis?.report) {
    return (
      <section className="rounded-md bg-white p-8 text-center shadow-soft">
        <AlertTriangle className="mx-auto mb-4 text-amber-500" size={38} />
        <h1 className="mb-2 text-2xl font-bold">No Report Yet</h1>
        <p className="mx-auto mb-6 max-w-xl text-slate-600">
          Upload an assignment PDF first to generate an academic integrity report.
        </p>
        <button
          className="rounded-md bg-ibm px-5 py-3 font-semibold text-white"
          onClick={() => onNavigate("upload")}
          type="button"
        >
          Go to Upload
        </button>
      </section>
    );
  }

  const report = analysis.analysis.report;
  const score = report.academic_integrity_score;
  const scoreColor =
    score >= 80 ? "text-green-700 bg-green-50" : score >= 60 ? "text-amber-700 bg-amber-50" : "text-red-700 bg-red-50";

  return (
    <div className="space-y-6">
      <section className="grid gap-5 rounded-md bg-white p-6 shadow-soft lg:grid-cols-[1fr_220px]">
        <div>
          <div className="mb-3 flex flex-wrap items-center gap-2">
            <span className="rounded-md bg-blue-50 px-3 py-2 text-sm font-semibold text-ibm">
              Report ID: {analysis.analysis.report_id}
            </span>
            {report.demo_mode && (
              <span className="rounded-md bg-amber-50 px-3 py-2 text-sm font-semibold text-amber-700">
                Demo Mode
              </span>
            )}
          </div>
          <h1 className="mb-3 text-3xl font-bold">Academic Integrity Report</h1>
          <p className="max-w-3xl leading-7 text-slate-600">{report.summary}</p>
          <p className="mt-4 text-sm text-slate-500">Model: {report.model_used}</p>
        </div>

        <div className={`flex flex-col items-center justify-center rounded-md p-5 ${scoreColor}`}>
          <BadgeCheck size={34} />
          <span className="mt-3 text-5xl font-bold">{score}</span>
          <span className="text-sm font-semibold">Integrity Score</span>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-2">
        {sections.map((section) => {
          const Icon = section.icon;
          return (
            <article key={section.key} className="rounded-md border border-slate-200 bg-white p-5">
              <div className="mb-4 flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-md bg-blue-50 text-ibm">
                  <Icon size={21} />
                </span>
                <h2 className="text-lg font-bold">{section.title}</h2>
              </div>
              <ul className="space-y-3">
                {report[section.key].map((item) => (
                  <li key={item} className="rounded-md bg-slate-50 p-3 leading-6 text-slate-700">
                    {item}
                  </li>
                ))}
              </ul>
            </article>
          );
        })}
      </section>
    </div>
  );
}
