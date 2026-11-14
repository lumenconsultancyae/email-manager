import React, { useState } from "react";

const SAMPLE_EMAILS = [
  {
    message_id: "msg-101",
    sender: "deals@promo-mart.example",
    subject: "Weekend Flash Sale - 60% Discount Newsletter",
    body: "Limited time promo offer! Click here to unsubscribe anytime.",
    age_days: 45,
    is_unread: false,
  },
  {
    message_id: "msg-102",
    sender: "ops@lumenconsultancy.ae",
    subject: "Re: Sprint Review & Client Deployment Milestone",
    body: "Please review the updated architecture before Friday deployment.",
    age_days: 1,
    is_unread: true,
  },
  {
    message_id: "msg-103",
    sender: "billing@cloud-infra.example",
    subject: "Monthly Invoice & Payment Receipt #4821",
    body: "Your November billing statement has been processed.",
    age_days: 4,
    is_unread: true,
  },
];

export default function App() {
  const [report, setReport] = useState(null);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 960, margin: "0 auto", padding: 32 }}>
      <header style={{ marginBottom: 24 }}>
        <h1 style={{ marginBottom: 8 }}>Smart Email Manager</h1>
        <p style={{ color: "#475569", margin: 0 }}>
          Intelligent inbox analysis powered by AGY containers — analyze emails, clean obsolete messages, and group threads by topic.
        </p>
      </header>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16, marginBottom: 24 }}>
        <div style={{ border: "1px solid #cbd5e1", borderRadius: 8, padding: 16 }}>
          <h3 style={{ marginTop: 0 }}>1. AGY Container Analysis</h3>
          <p style={{ fontSize: 14, color: "#475569" }}>
            Dispatches email batches to isolated AGY agent containers for priority scoring and thread summarization.
          </p>
        </div>
        <div style={{ border: "1px solid #cbd5e1", borderRadius: 8, padding: 16 }}>
          <h3 style={{ marginTop: 0 }}>2. Clean Old &amp; Useless Emails</h3>
          <p style={{ fontSize: 14, color: "#475569" }}>
            Detects stale promotions, expired newsletters, and low-value notifications for one-click archive or deletion.
          </p>
        </div>
        <div style={{ border: "1px solid #cbd5e1", borderRadius: 8, padding: 16 }}>
          <h3 style={{ marginTop: 0 }}>3. Topic Clustering</h3>
          <p style={{ fontSize: 14, color: "#475569" }}>
            Groups inbox messages into coherent topics (Work &amp; Projects, Finance &amp; Billing, Security, Promotions).
          </p>
        </div>
      </section>

      <section style={{ border: "1px solid #e2e8f0", borderRadius: 8, padding: 20 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <h2 style={{ margin: 0, fontSize: 18 }}>Sample Inbox Preview ({SAMPLE_EMAILS.length} messages)</h2>
          <button
            type="button"
            onClick={() =>
              setReport({
                total_analyzed: SAMPLE_EMAILS.length,
                useless_count: 1,
                topics: ["Work & Projects", "Finance & Billing", "Promotions & Newsletters"],
              })
            }
            style={{
              backgroundColor: "#0f172a",
              color: "#ffffff",
              border: "none",
              borderRadius: 6,
              padding: "8px 16px",
              cursor: "pointer",
            }}
          >
            Simulate AGY Analysis
          </button>
        </div>
        {report && (
          <div data-testid="analysis-summary" style={{ marginTop: 16, padding: 12, background: "#f8fafc", borderRadius: 6 }}>
            <strong>Analyzed:</strong> {report.total_analyzed} emails | <strong>Cleanup Candidates:</strong> {report.useless_count} |{" "}
            <strong>Topics:</strong> {report.topics.join(", ")}
          </div>
        )}
      </section>
    </main>
  );
}

