import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Sidebar,
  studentLinks,
  Card,
  Button,
  Badge,
} from "../components/Components.jsx";
import { reviews } from "../data.js";
import { getReview, submitReview, getToken } from "../api.js";

// Review Workflow Page - real status from the backend + a mock feedback timeline.
export default function ReviewWorkflowPage() {
  const navigate = useNavigate();

  // The 4 possible review statuses
  const statuses = ["Draft", "Needs Revision", "Ready", "Published"];

  const [currentStatus, setCurrentStatus] = useState("Draft");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  // The feedback timeline stays as sample data (coach features are out of scope).
  const myFeedback = reviews.filter((r) => r.studentId === "s1");

  // Load the real review status when the page opens.
  useEffect(() => {
    if (!getToken()) {
      navigate("/sign-in");
      return;
    }
    getReview()
      .then((r) => r && r.status && setCurrentStatus(r.status))
      .catch((err) => setError(err.message));
  }, [navigate]);

  // Pick a badge color based on the status
  function statusColor(status) {
    if (status === "Published") return "green";
    if (status === "Ready") return "teal";
    if (status === "Needs Revision") return "yellow";
    return "gray"; // Draft
  }

  async function changeStatus(newStatus, note) {
    setError("");
    try {
      const r = await submitReview(newStatus);
      setCurrentStatus(r.status);
      setMessage(note);
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      setError(err.message);
    }
  }

  function submitForReview() {
    changeStatus("Ready", "Submitted for review!");
  }

  function publishPortfolio() {
    changeStatus("Published", "Portfolio published!");
  }

  return (
    <div className="page-shell">
      <Sidebar title="Student" links={studentLinks} />

      <main className="page-main">
        <h1 className="page-header">Review Workflow</h1>

        {message && <p className="alert-success">{message}</p>}
        {error && <p className="alert-error">{error}</p>}

        {/* Status steps */}
        <Card className="mb-6">
          <h3 className="card-title">Status</h3>
          <div className="flex flex-wrap gap-2">
            {statuses.map((status) => (
              <Badge
                key={status}
                text={status}
                // Highlight the current status, others stay gray
                color={status === currentStatus ? statusColor(status) : "gray"}
              />
            ))}
          </div>

          <div className="mt-4 flex gap-2">
            <Button onClick={submitForReview}>Submit for Review</Button>
            <Button variant="teal" onClick={publishPortfolio}>
              Publish Portfolio
            </Button>
          </div>
        </Card>

        {/* Reviewer feedback timeline */}
        <Card>
          <h3 className="card-title mb-4">Feedback Timeline</h3>
          <div className="space-y-4">
            {myFeedback.map((item) => (
              <div key={item.id} className="timeline-item pl-4">
                <div className="flex items-center gap-2">
                  <Badge text={item.status} color={statusColor(item.status)} />
                  <span className="text-xs text-gray-400">{item.date}</span>
                </div>
                <p className="mt-1 text-sm font-medium text-gray-700">{item.reviewer}</p>
                <p className="text-sm text-gray-500">{item.comment}</p>
              </div>
            ))}
          </div>
        </Card>
      </main>
    </div>
  );
}
