import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Sidebar,
  studentLinks,
  Card,
  Input,
  Textarea,
  Button,
  AIBox,
} from "../components/Components.jsx";
import { projects, aiFeedback } from "../data.js";
import { ImagePlus } from "lucide-react";

// Add/Edit Project Page - one form used for BOTH adding and editing.
// If there is a :projectId in the URL we are editing, otherwise adding.
export default function AddEditProjectPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();

  // Find the project we are editing (if any)
  const editing = projects.find((p) => p.id === projectId);

  // Form state - fill it with the project data if editing
  const [title, setTitle] = useState(editing ? editing.title : "");
  const [summary, setSummary] = useState(editing ? editing.summary : "");
  const [description, setDescription] = useState(editing ? editing.description : "");
  const [tech, setTech] = useState(editing ? editing.techStack.join(", ") : "");
  const [github, setGithub] = useState(editing ? editing.github : "");
  const [demo, setDemo] = useState(editing ? editing.demo : "");
  const [status, setStatus] = useState(editing ? editing.status : "Draft");
  const [collaborators, setCollaborators] = useState(
    editing ? editing.collaborators.join(", ") : ""
  );
  const [saved, setSaved] = useState(false);

  // Fake save - shows a message then goes back to the projects list
  function handleSave(e) {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => navigate("/student/projects"), 1200);
  }

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Student" links={studentLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">
          {editing ? "Edit Project" : "Add Project"}
        </h1>

        <div className="grid gap-6 lg:grid-cols-3">
          {/* The form takes 2 columns */}
          <div className="lg:col-span-2">
            <Card>
              {saved && (
                <p className="mb-4 rounded-lg bg-green-50 p-2 text-sm text-green-700">
                  Project saved! Redirecting...
                </p>
              )}

              <form onSubmit={handleSave}>
                <Input label="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
                <Input
                  label="Summary"
                  value={summary}
                  onChange={(e) => setSummary(e.target.value)}
                />
                <Textarea
                  label="Description"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={5}
                />
                <Input
                  label="Tech Stack (comma separated)"
                  value={tech}
                  onChange={(e) => setTech(e.target.value)}
                />
                <Input
                  label="GitHub Link"
                  value={github}
                  onChange={(e) => setGithub(e.target.value)}
                />
                <Input label="Demo Link" value={demo} onChange={(e) => setDemo(e.target.value)} />

                {/* Screenshot uploader (fake UI only) */}
                <div className="mb-4">
                  <label className="mb-1 block text-sm font-medium text-gray-700">
                    Screenshots
                  </label>
                  <div className="flex flex-col items-center rounded-lg border-2 border-dashed border-gray-300 p-6 text-center">
                    <ImagePlus className="mb-2 h-7 w-7 text-gray-400" />
                    <p className="text-sm text-gray-500">Click to add screenshots</p>
                  </div>
                </div>

                {/* Status dropdown */}
                <div className="mb-4">
                  <label className="mb-1 block text-sm font-medium text-gray-700">Status</label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                  >
                    <option>Draft</option>
                    <option>Published</option>
                  </select>
                </div>

                {/* Collaborators */}
                <Input
                  label="Collaborators (comma separated)"
                  value={collaborators}
                  onChange={(e) => setCollaborators(e.target.value)}
                />

                <div className="flex gap-2">
                  <Button type="submit">Save Project</Button>
                  <Button variant="outline" onClick={() => navigate("/student/projects")}>
                    Cancel
                  </Button>
                </div>
              </form>
            </Card>
          </div>

          {/* AI summary helper on the side */}
          <div>
            <AIBox
              title="AI Project Summary"
              buttonLabel="Generate Summary"
              result={aiFeedback.projectSummary}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
