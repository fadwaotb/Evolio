import { useEffect, useRef, useState } from "react";
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
import { aiFeedback } from "../data.js";
import {
  getProject,
  createProject,
  updateProject,
  uploadProjectImage,
  fileUrl,
  getToken,
} from "../api.js";
import { ImagePlus, X } from "lucide-react";

// Add/Edit Project Page - one form used for BOTH adding and editing (real backend).
// If there is a :projectId in the URL we are editing, otherwise adding.
export default function AddEditProjectPage() {
  const { projectId } = useParams();
  const navigate = useNavigate();
  const editing = Boolean(projectId);

  // Form state (empty for "add"; filled from the backend for "edit")
  const [title, setTitle] = useState("");
  const [summary, setSummary] = useState("");
  const [description, setDescription] = useState("");
  const [tech, setTech] = useState("");
  const [github, setGithub] = useState("");
  const [demo, setDemo] = useState("");
  const [status, setStatus] = useState("Draft");
  const [collaborators, setCollaborators] = useState("");
  // `screenshot` is a preview URL (data URL for a new pick, or a server URL).
  const [screenshot, setScreenshot] = useState("");
  const [screenshotFile, setScreenshotFile] = useState(null); // the real File to upload
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");

  // Hidden file input we trigger by clicking the upload box
  const fileInputRef = useRef(null);

  // When editing, load the project from the backend and fill the form.
  useEffect(() => {
    if (!getToken()) {
      navigate("/sign-in");
      return;
    }
    if (!editing) return;
    getProject(projectId)
      .then((p) => {
        setTitle(p.title || "");
        setSummary(p.summary || "");
        setDescription(p.description || "");
        setTech((p.tech_stack || []).join(", "));
        setGithub(p.github_link || "");
        setDemo(p.demo_link || "");
        setStatus(p.status || "Draft");
        setCollaborators((p.collaborators || []).join(", "));
        if (p.screenshots && p.screenshots[0]) setScreenshot(fileUrl(p.screenshots[0]));
      })
      .catch((err) => setError(err.message));
  }, [editing, projectId, navigate]);

  // Read the chosen image into a data URL for preview AND keep the File to upload.
  function handleScreenshotChange(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    setScreenshotFile(file);
    const reader = new FileReader();
    reader.onload = () => setScreenshot(reader.result);
    reader.readAsDataURL(file);
  }

  // Real save: create or update the project, then upload the screenshot if any.
  async function handleSave(e) {
    e.preventDefault();
    setError("");
    const payload = {
      title,
      summary,
      description,
      tech_stack: tech.split(",").map((s) => s.trim()).filter(Boolean),
      github_link: github,
      demo_link: demo,
      status,
      collaborators: collaborators.split(",").map((s) => s.trim()).filter(Boolean),
    };
    try {
      const project = editing
        ? await updateProject(projectId, payload)
        : await createProject(payload);

      // Only upload if the user picked a NEW file this time.
      if (screenshotFile) {
        await uploadProjectImage(project.id, screenshotFile);
      }

      setSaved(true);
      setTimeout(() => navigate("/student/projects"), 1000);
    } catch (err) {
      setError(err.message);
    }
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
              {error && <p className="alert-error">{error}</p>}

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
                          setScreenshotFile(null);
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
