import { useState } from "react";
import {
  Sidebar,
  adminLinks,
  Card,
  Button,
} from "../components/Components.jsx";

// System Settings Page - simple platform configuration (mock toggles).
export default function SystemSettingsPage() {
  // Feature flags as simple on/off booleans
  const [features, setFeatures] = useState({
    aiFeedback: true,
    employerMessaging: true,
    publicPortfolios: false,
  });

  // Notification settings
  const [notifications, setNotifications] = useState({
    emailAlerts: true,
    weeklyReport: false,
  });

  // Access policy (a simple dropdown)
  const [accessPolicy, setAccessPolicy] = useState("Invite only");

  const [message, setMessage] = useState("");

  // Flip one feature flag on/off
  function toggleFeature(key) {
    setFeatures({ ...features, [key]: !features[key] });
  }

  function toggleNotification(key) {
    setNotifications({ ...notifications, [key]: !notifications[key] });
  }

  function saveSettings() {
    setMessage("Settings saved!");
    setTimeout(() => setMessage(""), 2000);
  }

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Admin" links={adminLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">System Settings</h1>

        {message && (
          <p className="mb-4 rounded-lg bg-green-50 p-2 text-sm text-green-700">{message}</p>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Feature flags */}
          <Card>
            <h3 className="mb-3 font-semibold text-gray-800">Feature Flags</h3>
            <Toggle
              label="AI Feedback"
              on={features.aiFeedback}
              onToggle={() => toggleFeature("aiFeedback")}
            />
            <Toggle
              label="Employer Messaging"
              on={features.employerMessaging}
              onToggle={() => toggleFeature("employerMessaging")}
            />
            <Toggle
              label="Public Portfolios"
              on={features.publicPortfolios}
              onToggle={() => toggleFeature("publicPortfolios")}
            />
          </Card>

          {/* Notification settings */}
          <Card>
            <h3 className="mb-3 font-semibold text-gray-800">Notifications</h3>
            <Toggle
              label="Email Alerts"
              on={notifications.emailAlerts}
              onToggle={() => toggleNotification("emailAlerts")}
            />
            <Toggle
              label="Weekly Report"
              on={notifications.weeklyReport}
              onToggle={() => toggleNotification("weeklyReport")}
            />
          </Card>

          {/* Access policy */}
          <Card>
            <h3 className="mb-3 font-semibold text-gray-800">Access Policy</h3>
            <select
              value={accessPolicy}
              onChange={(e) => setAccessPolicy(e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
            >
              <option>Invite only</option>
              <option>Open registration</option>
              <option>Admin approval required</option>
            </select>
          </Card>
        </div>

        <div className="mt-6">
          <Button onClick={saveSettings}>Save Settings</Button>
        </div>
      </main>
    </div>
  );
}

// Small reusable toggle row used only on this page.
function Toggle({ label, on, onToggle }) {
  return (
    <div className="mb-3 flex items-center justify-between">
      <span className="text-sm text-gray-700">{label}</span>
      {/* A simple button that acts like an on/off switch */}
      <button
        onClick={onToggle}
        className={`h-6 w-11 rounded-full p-1 transition ${on ? "bg-teal-500" : "bg-gray-300"}`}
      >
        <span
          className={`block h-4 w-4 rounded-full bg-white transition ${on ? "translate-x-5" : ""}`}
        ></span>
      </button>
    </div>
  );
}
