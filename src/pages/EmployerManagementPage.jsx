import { useState } from "react";
import {
  Sidebar,
  adminLinks,
  Card,
  Button,
  Badge,
  StatCard,
} from "../components/Components.jsx";
import { employers as initialEmployers } from "../data.js";

// Employer Management Page - admin approves employers and sees activity.
export default function EmployerManagementPage() {
  // Keep employers in state so we can change their status
  const [employers, setEmployers] = useState(initialEmployers);

  // Approve a pending employer
  function approve(id) {
    setEmployers(
      employers.map((e) => (e.id === id ? { ...e, status: "Approved" } : e))
    );
  }

  // Count how many are approved (for the summary)
  const approvedCount = employers.filter((e) => e.status === "Approved").length;

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Admin" links={adminLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Employer Management</h1>

        {/* Activity overview */}
        <div className="mb-6 grid gap-4 sm:grid-cols-3">
          <StatCard label="Total Employers" value={employers.length} />
          <StatCard label="Approved" value={approvedCount} accent="teal" />
          <StatCard label="Pending" value={employers.length - approvedCount} />
        </div>

        {/* Employer directory */}
        <Card>
          <h3 className="mb-4 font-semibold text-gray-800">Employer Directory</h3>
          <div className="space-y-3">
            {employers.map((employer) => (
              <div
                key={employer.id}
                className="flex flex-col gap-2 rounded-lg border border-gray-100 p-3 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <p className="font-medium text-gray-800">{employer.company}</p>
                  <p className="text-xs text-gray-500">
                    {employer.name} • {employer.openRoles} open roles •{" "}
                    {employer.candidatesViewed} candidates viewed
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <Badge
                    text={employer.status}
                    color={employer.status === "Approved" ? "green" : "yellow"}
                  />
                  {/* Only show approve button if still pending */}
                  {employer.status === "Pending" && (
                    <Button onClick={() => approve(employer.id)}>Approve</Button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </main>
    </div>
  );
}
