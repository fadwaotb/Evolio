import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Sidebar,
  employerLinks,
  Card,
  Button,
  Badge,
  Textarea,
  Modal,
  ErrorState,
  LoadingState,
} from "../components/Components.jsx";
import { students, projects, aiFeedback } from "../data.js";
import { Github, ExternalLink, Bot } from "lucide-react";

// Portfolio Viewer Page - how an employer sees a student's full portfolio.
export default function PortfolioViewerPage() {
  const { studentId } = useParams();
  const navigate = useNavigate();

  // Find the student from the URL id
  const student = students.find((s) => s.id === studentId);
  const studentProjects = student ? projects.filter((p) => p.studentId === student.id) : [];

  // Local state for feedback box + save + bot
  const [feedback, setFeedback] = useState("");
  const [feedbackSent, setFeedbackSent] = useState(false);
  const [saved, setSaved] = useState(false);
  const [botOpen, setBotOpen] = useState(false);
  const [botLoading, setBotLoading] = useState(false);

  // If the student id is wrong, show an error state
  if (!student) {
    return (
      <div className="flex flex-col md:flex-row">
        <Sidebar title="Employer" links={employerLinks} />
        <main className="flex-1 p-6">
          <ErrorState message="Sorry, we could not find this candidate." />
        </main>
      </div>
    );
  }

  function sendFeedback() {
    setFeedbackSent(true);
    setFeedback("");
    setTimeout(() => setFeedbackSent(false), 2000);
  }

  function askBot() {
    setBotOpen(true);
    setBotLoading(true);
    setTimeout(() => setBotLoading(false), 1500);
  }

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Employer" links={employerLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Candidate Portfolio</h1>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* Left: profile, resume, projects */}
          <div className="space-y-6 lg:col-span-2">
            {/* Profile */}
            <Card>
              <div className="flex items-center gap-4">
                <div
                  className={`flex h-16 w-16 items-center justify-center rounded-full text-xl font-bold text-white ${student.avatarColor}`}
                >
                  {student.name.charAt(0)}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">{student.name}</h2>
                  <p className="text-sm text-gray-500">{student.headline}</p>
                  <Badge text={student.availability} color="green" />
                </div>
              </div>
              <p className="mt-4 text-sm text-gray-600">{student.bio}</p>
            </Card>

            {/* Resume preview */}
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Resume</h3>
              <div className="flex h-40 items-center justify-center rounded-lg bg-gray-100 text-sm text-gray-400">
                Resume preview (mock)
              </div>
              <div className="mt-3">
                <Button variant="outline">Download Resume</Button>
              </div>
            </Card>

            {/* Projects with evaluation note */}
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Projects</h3>
              <div className="space-y-4">
                {studentProjects.map((p) => (
                  <div key={p.id} className="rounded-lg border border-gray-100 p-4">
                    <h4 className="font-medium text-gray-800">{p.title}</h4>
                    <p className="text-sm text-gray-500">{p.summary}</p>

                    {/* Collaborator links */}
                    {p.collaborators.length > 0 && (
                      <p className="mt-1 text-xs text-gray-400">
                        Collaborators: {p.collaborators.join(", ")}
                      </p>
                    )}

                    <div className="mt-2 flex gap-3 text-sm">
                      <a href={p.github} className="flex items-center gap-1 text-blue-600">
                        <Github className="h-4 w-4" /> Code
                      </a>
                      {p.demo && (
                        <a href={p.demo} className="flex items-center gap-1 text-teal-600">
                          <ExternalLink className="h-4 w-4" /> Demo
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Right: actions, feedback, bot */}
          <div className="space-y-6">
            {/* Quick actions */}
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Actions</h3>
              <div className="flex flex-col gap-2">
                <Button onClick={() => navigate("/employer/messages")}>Contact Student</Button>
                <Button variant="teal" onClick={() => setSaved(!saved)}>
                  {saved ? "Saved ✓" : "Save Candidate"}
                </Button>
              </div>
            </Card>

            {/* Leave feedback */}
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Leave Feedback</h3>
              {feedbackSent && (
                <p className="mb-2 rounded-lg bg-green-50 p-2 text-sm text-green-700">
                  Feedback sent!
                </p>
              )}
              <Textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                placeholder="Write your feedback..."
              />
              <Button onClick={sendFeedback}>Send</Button>
            </Card>

            {/* Ask About This Candidate bot */}
            <Card>
              <div className="mb-3 flex items-center gap-2">
                <Bot className="h-5 w-5 text-blue-600" />
                <h3 className="font-semibold text-gray-800">Ask About This Candidate</h3>
              </div>
              <Button onClick={askBot}>Ask the Bot</Button>
            </Card>
          </div>
        </div>
      </main>

      {/* Bot modal (fake AI) */}
      <Modal open={botOpen} onClose={() => setBotOpen(false)} title="Candidate Bot">
        {botLoading ? (
          <LoadingState message="Bot is thinking..." />
        ) : (
          <div>
            <p className="mb-4 text-sm text-gray-700">{aiFeedback.candidateBotAnswer}</p>
            <Button onClick={() => setBotOpen(false)}>Close</Button>
          </div>
        )}
      </Modal>
    </div>
  );
}
