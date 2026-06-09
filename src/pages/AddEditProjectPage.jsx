import { useRef, useState } from "react";
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
import { ImagePlus, X } from "lucide-react";

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
  // Screenshot is stored as a data URL so it can be previewed without a backend.
  // Projects keep a `screenshots` array; here we edit the primary (first) one.
  const [screenshot, setScreenshot] = useState(
    editing && editing.screenshots ? editing.screenshots[0] || "" : ""
  );
  const [saved, setSaved] = useState(false);

  // Hidden file input we trigger by clicking the upload box
  const fileInputRef = useRef(null);

  // Read the chosen image file into a data URL so we can preview it
  function handleScreenshotChange(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = () => setScreenshot(reader.result);
    reader.readAsDataURL(file);
  }

  // Fake save - shows a message then goes back to the projects list
  function handleSave(e) {
    e.preventDefault();
    // No backend: persist the screenshot onto the mock project so it shows
    // up in the projects list and portfolio previews during this session.
    if (editing) {
      const rest = (editing.screenshots || []).slice(1);
      editing.screenshots = screenshot ? [screenshot, ...rest] : rest;
    }
    setSaved(true);
    setTimeout(() => navigate("/student/projects"), 1200);
  }

  return (
    <div className="page-shell">
      <Sidebar title="Student" links={studentLinks} />

      <main className="page-main">
        <h1 className="page-header">
          {editing ? "Edit Project" : "Add Project"}
        </h1>

        <div className="content-grid-3">
          {/* The form takes 2 columns */}
          <div className="lg:col-span-2">
            <Card>
              {saved && <p className="alert-success">Project saved! Redirecting...</p>}

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

                {/* Screenshot uploader */}
                <div className="mb-4">
                  <label className="form-label">Screenshot</label>

                  {/* Hidden file input, triggered by clicking the box below */}
                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={handleScreenshotChange}
                  />

                  {screenshot ? (
                    // Preview the chosen screenshot with a remove button
                    <div className="relative">
                      <img
                        src={screenshot}
                        alt="Project screenshot preview"
                        className="w-full rounded-lg border border-gray-200 object-cover"
                      />
                      <button
                        type="button"
                        onClick={() => {
                          setScreenshot("");
                          if (fileInputRef.current) fileInputRef.current.value = "";
                        }}
                        className="absolute right-2 top-2 rounded-full bg-white/90 p-1 text-gray-600 shadow hover:bg-white"
                        aria-label="Remove screenshot"
                      >
                        <X className="h-4 w-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => fileInputRef.current && fileInputRef.current.click()}
                        className="mt-2 text-sm text-[#199DB2] hover:underline"
                      >
                        Replace screenshot
                      </button>
                    </div>
                  ) : (
                    <div
                      role="button"
                      tabIndex={0}
                      onClick={() => fileInputRef.current && fileInputRef.current.click()}
                      onKeyDown={(e) => {
                        if (e.key === "Enter" || e.key === " ")
                          fileInputRef.current && fileInputRef.current.click();
                      }}
                      className="upload-box cursor-pointer p-6 hover:border-[#3199CC]"
                    >
                      <ImagePlus className="mb-2 h-7 w-7 text-gray-400" />
                      <p className="text-sm text-gray-500">Click to add a screenshot</p>
                    </div>
                  )}
                </div>

                {/* Status dropdown */}
                <div className="mb-4">
                  <label className="form-label">Status</label>
                  <select
                    value={status}
                    onChange={(e) => setStatus(e.target.value)}
                    className="form-input"
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
