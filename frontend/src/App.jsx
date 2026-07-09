// Main application shell with lightweight page routing for the AIIP demo.
import React from "react";
import { useMemo, useState } from "react";
import { BookOpenCheck, FileUp, Home, ShieldCheck } from "lucide-react";
import HomePage from "./pages/HomePage.jsx";
import UploadPage from "./pages/UploadPage.jsx";
import ReportPage from "./pages/ReportPage.jsx";

const navItems = [
  { id: "home", label: "Home", icon: Home },
  { id: "upload", label: "Upload", icon: FileUp },
  { id: "report", label: "Report", icon: BookOpenCheck },
];

export default function App() {
  // Store the latest generated report so the report page can render instantly.
  const [activePage, setActivePage] = useState("home");
  const [analysis, setAnalysis] = useState(null);

  const ActivePage = useMemo(() => {
    if (activePage === "upload") return UploadPage;
    if (activePage === "report") return ReportPage;
    return HomePage;
  }, [activePage]);

  function handleReportReady(nextAnalysis) {
    // Save the generated report and move the user to the report page.
    setAnalysis(nextAnalysis);
    setActivePage("report");
  }

  return (
    <div className="min-h-screen bg-panel text-ink">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-5 py-5 md:flex-row md:items-center md:justify-between">
          <button
            className="flex items-center gap-3 text-left"
            onClick={() => setActivePage("home")}
            type="button"
          >
            <span className="flex h-11 w-11 items-center justify-center rounded-md bg-ibm text-white">
              <ShieldCheck size={24} />
            </span>
            <span>
              <span className="block text-lg font-bold">AIIP</span>
              <span className="text-sm text-slate-600">Academic Integrity Intelligence Platform</span>
            </span>
          </button>

          <nav className="flex flex-wrap gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  className={`flex h-10 items-center gap-2 rounded-md px-4 text-sm font-semibold transition ${
                    isActive
                      ? "bg-ibm text-white"
                      : "bg-slate-100 text-slate-700 hover:bg-slate-200"
                  }`}
                  onClick={() => setActivePage(item.id)}
                  type="button"
                >
                  <Icon size={17} />
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-5 py-8">
        <ActivePage
          analysis={analysis}
          onNavigate={setActivePage}
          onReportReady={handleReportReady}
        />
      </main>
    </div>
  );
}
