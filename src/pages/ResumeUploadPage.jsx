import { useState } from "react";
import {
  Sidebar,
  studentLinks,
  Card,
  Button,
  AIBox,
  Badge,
} from "../components/Components.jsx";
import { resumes, aiFeedback } from "../data.js";
import { FileText, Upload } from "lucide-react";

// Resume Upload Page - upload/replace a resume + view a mock AI review.
export default function ResumeUploadPage() {
  // Use the first resume as the current one (mock data)
  const [resume, setResume] = useState(resumes[0]);
  const [message, setMessage] = useState("");

  // Fake "upload/replace" - just updates the file name and date
  function handleUpload() {
    setResume({
      ...resume,
      fileName: "Updated_Resume.pdf",
      uploadedDate: "2026-06-08",
    });
    setMessage("Resume uploaded successfully!");
    setTimeout(() => setMessage(""), 2000);
  }

  return (
    <div className="page-shell">
      <Sidebar title="Student" links={studentLinks} />

      <main className="page-main">
        <h1 className="page-header">Resume</h1>

        {message && <p className="alert-success">{message}</p>}

        <div className="content-grid">
          {/* Upload area + metadata */}
          <div className="space-y-6">
            <Card>
              <h3 className="card-title">Upload / Replace Resume</h3>
              {/* Fake drag-and-drop box */}
              <div className="upload-box p-8">
                <Upload className="mb-2 h-8 w-8 text-gray-400" />
                <p className="text-sm text-gray-500">Drag a PDF here, or click to upload</p>
                <div className="mt-3">
                  <Button onClick={handleUpload}>Upload Resume</Button>
                </div>
              </div>
            </Card>

            {/* Resume metadata card */}
            <Card>
              <h3 className="card-title">Resume Details</h3>
              <div className="flex items-center gap-3">
                <FileText className="h-8 w-8 text-[#001776]" />
                <div>
                  <p className="font-medium text-gray-800">{resume.fileName}</p>
                  <p className="text-xs text-gray-500">
                    Uploaded {resume.uploadedDate} • {resume.sizeKb} KB
                  </p>
                </div>
              </div>
              <div className="mt-3 flex items-center gap-2">
                <Badge text={`${resume.downloads} downloads`} color="teal" />
                <Button variant="outline">Download</Button>
              </div>
            </Card>
          </div>

          {/* Preview + AI review */}
          <div className="space-y-6">
            {/* Simple preview box */}
            <Card>
              <h3 className="card-title">Preview</h3>
              <div className="preview-box h-48">Resume preview (mock)</div>
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
