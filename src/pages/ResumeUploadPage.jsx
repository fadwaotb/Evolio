import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Sidebar,
  studentLinks,
  Card,
  Button,
  AIBox,
  Badge,
} from "../components/Components.jsx";
import { aiFeedback } from "../data.js";
import {
  getResume,
  uploadResume,
  deleteResume,
  fileUrl,
  getToken,
} from "../api.js";
import { FileText, Upload } from "lucide-react";

// Resume Upload Page - real upload/replace/download/delete + a mock AI review.
export default function ResumeUploadPage() {
  const navigate = useNavigate();
  const [resume, setResume] = useState(null); // backend metadata or null
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  // Load the current resume metadata when the page opens.
  useEffect(() => {
    if (!getToken()) {
      navigate("/sign-in");
      return;
    }
    getResume()
      .then((r) => setResume(r))
      .catch((err) => setError(err.message));
  }, [navigate]);

  // Real upload: send the chosen file to the backend.
  async function handleFileChange(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    setError("");
    try {
      const data = await uploadResume(file);
      setResume(data);
      setMessage("Resume uploaded successfully!");
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      setError(err.message);
    }
  }

  function handleDownload() {
    if (resume) window.open(fileUrl(resume.url), "_blank");
  }

  async function handleDelete() {
    setError("");
    try {
      await deleteResume();
      setResume(null);
      setMessage("Resume deleted.");
      setTimeout(() => setMessage(""), 2000);
    } catch (err) {
      setError(err.message);
    }
  }

  // ISO date string -> just the YYYY-MM-DD part
  const uploadedDate = resume?.uploaded_at ? String(resume.uploaded_at).slice(0, 10) : "";

  return (
    <div className="page-shell">
      <Sidebar title="Student" links={studentLinks} />

      <main className="page-main">
        <h1 className="page-header">Resume</h1>

        {message && <p className="alert-success">{message}</p>}
        {error && <p className="alert-error">{error}</p>}

        <div className="content-grid">
          {/* Upload area + metadata */}
          <div className="space-y-6">
            <Card>
              <h3 className="card-title">Upload / Replace Resume</h3>

              {/* Hidden real file input, triggered by the box below */}
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,.doc,.docx"
                className="hidden"
                onChange={handleFileChange}
              />

              <div
                role="button"
                tabIndex={0}
                onClick={() => fileInputRef.current && fileInputRef.current.click()}
                onKeyDown={(e) => {
                  if (e.key === "Enter" || e.key === " ")
                    fileInputRef.current && fileInputRef.current.click();
                }}
                className="upload-box cursor-pointer p-8 hover:border-[#3199CC]"
              >
                <Upload className="mb-2 h-8 w-8 text-gray-400" />
                <p className="text-sm text-gray-500">Click to upload a PDF or Word file</p>
              </div>
            </Card>

            {/* Resume metadata card */}
            <Card>
              <h3 className="card-title">Resume Details</h3>
              {resume ? (
                <>
                  <div className="flex items-center gap-3">
                    <FileText className="h-8 w-8 text-[#001776]" />
                    <div>
                      <p className="font-medium text-gray-800">{resume.original_name}</p>
                      <p className="text-xs text-gray-500">
                        Uploaded {uploadedDate} • {resume.size_kb} KB
                      </p>
                    </div>
                  </div>
                  <div className="mt-3 flex items-center gap-2">
                    <Badge text={resume.content_type || "file"} color="teal" />
                    <Button variant="outline" onClick={handleDownload}>
                      Download
                    </Button>
                    <Button variant="danger" onClick={handleDelete}>
                      Delete
                    </Button>
                  </div>
                </>
              ) : (
                <p className="text-sm text-gray-500">No resume uploaded yet.</p>
              )}
            </Card>
          </div>

          {/* Preview + AI review */}
          <div className="space-y-6">
            {/* Simple preview box */}
            <Card>
              <h3 className="card-title">Preview</h3>
              {resume && resume.content_type === "application/pdf" ? (
                <iframe
                  title="Resume preview"
                  src={fileUrl(resume.url)}
                  className="h-48 w-full rounded-lg border border-gray-200"
                />
              ) : (
                <div className="preview-box h-48">
                  {resume ? "Preview available for PDF files" : "Upload a resume to preview"}
                </div>
              )}
            </Card>

            {/* AI resume review panel (fake AI) */}
            <AIBox
              title="AI Resume Review"
              buttonLabel="Review My Resume"
              result={aiFeedback.resumeReview}
            />
          </div>
        </div>
      </main>
    </div>
  );
}
