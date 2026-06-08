import { useState } from "react";
import {
  Sidebar,
  studentLinks,
  Card,
  Input,
  Textarea,
  Button,
} from "../components/Components.jsx";
import { students } from "../data.js";

// Profile Editor Page - lets a student edit their profile info.
export default function ProfileEditorPage() {
  // Start the form with the first student's data (mock "logged in" user)
  const me = students[0];

  const [name, setName] = useState(me.name);
  const [headline, setHeadline] = useState(me.headline);
  const [bio, setBio] = useState(me.bio);
  const [skills, setSkills] = useState(me.skills.join(", "));
  const [location, setLocation] = useState(me.location);
  const [github, setGithub] = useState(me.github);
  const [linkedin, setLinkedin] = useState(me.linkedin);
  const [contactEmail, setContactEmail] = useState(me.email);
  const [availability, setAvailability] = useState(me.availability);
  const [saved, setSaved] = useState(false);

  // Fake save - just shows a success message
  function handleSave(e) {
    e.preventDefault();
    setSaved(true);
    // Hide the message after 2 seconds
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Student" links={studentLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Edit Profile</h1>

        <Card className="max-w-2xl">
          {/* Success message after saving */}
          {saved && (
            <p className="mb-4 rounded-lg bg-green-50 p-2 text-sm text-green-700">
              Profile saved successfully!
            </p>
          )}

          <form onSubmit={handleSave}>
            <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <Input
              label="Headline"
              value={headline}
              onChange={(e) => setHeadline(e.target.value)}
            />
            <Textarea label="Bio" value={bio} onChange={(e) => setBio(e.target.value)} />
            <Input
              label="Skills (comma separated)"
              value={skills}
              onChange={(e) => setSkills(e.target.value)}
            />
            <Input
              label="Location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
            <Input label="GitHub" value={github} onChange={(e) => setGithub(e.target.value)} />
            <Input
              label="LinkedIn"
              value={linkedin}
              onChange={(e) => setLinkedin(e.target.value)}
            />
            <Input
              label="Contact Email"
              type="email"
              value={contactEmail}
              onChange={(e) => setContactEmail(e.target.value)}
            />

            {/* Availability status dropdown */}
            <div className="mb-4">
              <label className="mb-1 block text-sm font-medium text-gray-700">
                Availability Status
              </label>
              <select
                value={availability}
                onChange={(e) => setAvailability(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
              >
                <option>Open to work</option>
                <option>Interviewing</option>
                <option>Not looking</option>
              </select>
            </div>

            <Button type="submit">Save Profile</Button>
          </form>
        </Card>
      </main>
    </div>
  );
}
