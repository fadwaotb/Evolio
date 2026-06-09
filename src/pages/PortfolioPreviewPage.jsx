import { useState } from "react";
import {
  Sidebar,
  studentLinks,
  Card,
  Button,
  Badge,
  Input,
  Modal,
  AIBox,
  LoadingState,
} from "../components/Components.jsx";
import { students, projects, aiFeedback } from "../data.js";
import { Github, ExternalLink, Bot } from "lucide-react";

// Portfolio Preview Page - shows how the student's public portfolio looks.
export default function PortfolioPreviewPage() {
  const me = students[0]; // mock logged-in student
  const myProjects = projects.filter((p) => p.studentId === me.id);
  const featured = myProjects.filter((p) => p.featured);

  // "Ask About This Candidate" bot modal
  const [botOpen, setBotOpen] = useState(false);
  const [botLoading, setBotLoading] = useState(false);

  // Shareable link toggle
  const [isPublic, setIsPublic] = useState(true);

  function askBot() {
    setBotOpen(true);
    setBotLoading(true);
    setTimeout(() => setBotLoading(false), 1500);
  }

  return (
    <div className="page-shell">
      <Sidebar title="Student" links={studentLinks} />

      <main className="page-main">
        <h1 className="page-header">Portfolio Preview</h1>

        <div className="content-grid-3">
          {/* Left: profile + projects (2 columns) */}
          <div className="space-y-6 lg:col-span-2">
            {/* Profile header */}
            <Card>
              <div className="flex items-center gap-4">
                <div className={`avatar ${me.avatarColor}`}>
                  {me.name.charAt(0)}
                </div>
                <div>
                  <h2 className="text-xl font-bold text-gray-800">{me.name}</h2>
                  <p className="text-sm text-gray-500">{me.headline}</p>
                  <div className="mt-1">
                    <Badge text={me.availability} color="green" />
                  </div>
                </div>
              </div>
              <p className="mt-4 text-sm text-gray-600">{me.bio}</p>

              <div className="mt-4 flex flex-wrap gap-2">
                <Button>Download Resume</Button>
                <Button variant="outline">Contact Student</Button>
              </div>
            </Card>

            {/* Skills */}
            <Card>
              <h3 className="card-title">Skills</h3>
              <div className="flex flex-wrap gap-2">
                {me.skills.map((skill) => (
                  <Badge key={skill} text={skill} color="blue" />
                ))}
              </div>
            </Card>

            {/* Featured projects */}
            <Card>
              <h3 className="card-title">Featured Projects</h3>
              <div className="space-y-4">
                {featured.map((p) => (
                  <div key={p.id} className="project-item">
                    <h4 className="font-medium text-gray-800">{p.title}</h4>
                    <p className="text-sm text-gray-500">{p.summary}</p>

                    {/* Collaborators */}
                    {p.collaborators.length > 0 && (
                      <p className="mt-1 text-xs text-gray-400">
                        With: {p.collaborators.join(", ")}
                      </p>
                    )}

                    <div className="mt-2 flex gap-3 text-sm">
                      <a href={p.github} className="flex items-center gap-1 text-[#001776]">
                        <Github className="h-4 w-4" /> Code
                      </a>
                      {p.demo && (
                        <a href={p.demo} className="flex items-center gap-1 text-[#199DB2]">
                          <ExternalLink className="h-4 w-4" /> Demo
                        </a>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Right: stats, share settings, AI, bot */}
          <div className="space-y-6">
            {/* Portfolio views */}
            <Card>
              <p className="text-sm text-gray-500">Portfolio Views</p>
              <p className="mt-1 text-2xl font-bold text-[#001776]">{me.portfolioViews}</p>
            </Card>

            {/* Shareable link settings */}
            <Card>
              <h3 className="card-title">Shareable Link</h3>
              <Input value="https://evolio.app/p/aisha" onChange={() => {}} />
              <label className="flex items-center gap-2 text-sm text-gray-600">
                <input
                  type="checkbox"
                  checked={isPublic}
                  onChange={(e) => setIsPublic(e.target.checked)}
                />
                Make portfolio public
              </label>
            </Card>

            {/* AI portfolio score */}
            <AIBox
              title="AI Portfolio Score"
              buttonLabel="Score My Portfolio"
              result={`Score: ${aiFeedback.portfolioScore}/100. ${aiFeedback.portfolioScoreText}`}
            />

            {/* Ask About This Candidate bot */}
            <Card>
              <div className="mb-3 flex items-center gap-2">
                <Bot className="h-5 w-5 text-[#001776]" />
                <h3 className="font-semibold text-gray-800">Ask About This Candidate</h3>
              </div>
              <p className="mb-3 text-sm text-gray-500">
                Employers can ask the AI bot questions about this candidate.
              </p>
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
