import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {
  Sidebar,
  studentLinks,
  Card,
  Button,
  Badge,
  Input,
  Modal,
  EmptyState,
  LoadingState,
} from "../components/Components.jsx";
import { projects as allProjects, aiFeedback } from "../data.js";

// Projects List Page - shows the student's projects with search/filter
// plus add/edit/delete and a fake "Enhance with AI" feedback modal.
export default function ProjectsListPage() {
  const navigate = useNavigate();

  // Keep projects in state so we can "delete" them (mock only)
  // Only show projects that belong to student s1 (our mock user)
  const [projects, setProjects] = useState(
    allProjects.filter((p) => p.studentId === "s1")
  );

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All"); // All / Published / Draft

  // AI modal state
  const [aiOpen, setAiOpen] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);

  // Delete a project from the list
  function deleteProject(id) {
    setProjects(projects.filter((p) => p.id !== id));
  }

  // Open the AI feedback modal and fake a loading delay
  function openAIFeedback() {
    setAiOpen(true);
    setAiLoading(true);
    setTimeout(() => setAiLoading(false), 1500);
  }

  // Filter projects by search text AND status
  const visibleProjects = projects.filter((p) => {
    const matchesSearch = p.title.toLowerCase().includes(search.toLowerCase());
    const matchesFilter = filter === "All" || p.status === filter;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Student" links={studentLinks} />

      <main className="flex-1 p-6">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-gray-800">My Projects</h1>
          <Link to="/student/projects/new">
            <Button>+ Add Project</Button>
          </Link>
        </div>

        {/* Search + filter controls */}
        <div className="mb-6 flex flex-col gap-3 sm:flex-row">
          <div className="flex-1">
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search projects..."
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="h-10 rounded-lg border border-gray-300 px-3 text-sm focus:border-blue-500 focus:outline-none"
          >
            <option>All</option>
            <option>Published</option>
            <option>Draft</option>
          </select>
        </div>

        {/* Featured projects note */}
        {visibleProjects.some((p) => p.featured) && (
          <p className="mb-3 text-sm text-gray-500">⭐ Featured projects show on your portfolio.</p>
        )}

        {/* Project list OR empty state */}
        {visibleProjects.length === 0 ? (
          <EmptyState message="No projects found. Try adding one!" />
        ) : (
          <div className="grid gap-4 md:grid-cols-2">
            {visibleProjects.map((project) => (
              <Card key={project.id}>
                <div className="mb-2 flex items-center justify-between">
                  <h3 className="font-semibold text-gray-800">{project.title}</h3>
                  {project.featured && <Badge text="Featured" color="teal" />}
                </div>
                <p className="mb-3 text-sm text-gray-500">{project.summary}</p>

                {/* Tech stack tags */}
                <div className="mb-3 flex flex-wrap gap-1">
                  {project.techStack.map((tech) => (
                    <Badge key={tech} text={tech} color="gray" />
                  ))}
                </div>

                <Badge
                  text={project.status}
                  color={project.status === "Published" ? "green" : "yellow"}
                />

                {/* Action buttons */}
                <div className="mt-4 flex flex-wrap gap-2">
                  <Button
                    variant="outline"
                    onClick={() => navigate(`/student/projects/${project.id}/edit`)}
                  >
                    Edit
                  </Button>
                  <Button variant="danger" onClick={() => deleteProject(project.id)}>
                    Delete
                  </Button>
                  <Button variant="teal" onClick={openAIFeedback}>
                    Enhance with AI
                  </Button>
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* AI feedback modal (fake AI) */}
      <Modal open={aiOpen} onClose={() => setAiOpen(false)} title="AI Project Feedback">
        {aiLoading ? (
          <LoadingState message="AI is reviewing your project..." />
        ) : (
          <div>
            <p className="mb-4 text-sm text-gray-700">{aiFeedback.projectFeedback}</p>
            <Button onClick={() => setAiOpen(false)}>Got it</Button>
          </div>
        )}
      </Modal>
    </div>
  );
}
