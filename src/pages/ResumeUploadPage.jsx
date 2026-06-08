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
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Student" links={studentLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Resume</h1>

        {message && (
          <p className="mb-4 rounded-lg bg-green-50 p-2 text-sm text-green-700">{message}</p>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Upload area + metadata */}
          <div className="space-y-6">
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Upload / Replace Resume</h3>
              {/* Fake drag-and-drop box */}
              <div className="flex flex-col items-center rounded-lg border-2 border-dashed border-gray-300 p-8 text-center">
                <Upload className="mb-2 h-8 w-8 text-gray-400" />
                <p className="text-sm text-gray-500">Drag a PDF here, or click to upload</p>
                <div className="mt-3">
                  <Button onClick={handleUpload}>Upload Resume</Button>
                </div>
              </div>
            </Card>

            {/* Resume metadata card */}
            <Card>
              <h3 className="mb-3 font-semibold text-gray-800">Resume Details</h3>
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
              <h3 className="mb-3 font-semibold text-gray-800">Preview</h3>
              <div className="flex h-48 items-center justify-center rounded-lg bg-gray-100 text-sm text-gray-400">
                Resume preview (mock)
              </div>
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
