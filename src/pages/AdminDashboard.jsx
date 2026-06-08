import {
  Sidebar,
  adminLinks,
  Card,
  StatCard,
  Badge,
} from "../components/Components.jsx";
import { analytics, reportedContent } from "../data.js";

// Admin Dashboard - platform-wide metrics and alerts.
export default function AdminDashboard() {
  const stats = analytics.admin;

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Admin" links={adminLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Admin Dashboard</h1>

        {/* Platform metrics */}
        <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard label="Total Users" value={stats.totalUsers} />
          <StatCard label="Students" value={stats.totalStudents} accent="teal" />
          <StatCard label="Employers" value={stats.totalEmployers} />
          <StatCard label="Coaches" value={stats.totalCoaches} accent="teal" />
        </div>

        <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard label="Published Portfolios" value={stats.publishedPortfolios} />
          <StatCard label="User Growth" value={stats.userGrowth} accent="teal" />
          <StatCard label="Employer Engagement" value={stats.employerEngagement} />
          <StatCard label="Moderation Alerts" value={stats.moderationAlerts} accent="teal" />
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Review workflow analytics (simple text bars) */}
          <Card>
            <h3 className="mb-4 font-semibold text-gray-800">Review Workflow</h3>
            <div className="space-y-3 text-sm">
              {/* Each bar is a simple div with a width */}
              <ReviewBar label="Draft" percent={20} />
              <ReviewBar label="Needs Revision" percent={35} />
              <ReviewBar label="Ready" percent={25} />
              <ReviewBar label="Published" percent={20} />
            </div>
          </Card>

          {/* Moderation alerts */}
          <Card>
            <h3 className="mb-4 font-semibold text-gray-800">Moderation Alerts</h3>
            <div className="space-y-3">
              {reportedContent.map((item) => (
                <div
                  key={item.id}
                  className="flex items-center justify-between rounded-lg border border-gray-100 p-3"
                >
                  <div>
                    <p className="text-sm font-medium text-gray-800">{item.type}</p>
                    <p className="text-xs text-gray-500">{item.reason}</p>
                  </div>
                  <Badge text={item.status} color="yellow" />
                </div>
              ))}
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}

// Small helper component for a labeled progress bar.
// (Kept in this file because it is only used here.)
function ReviewBar({ label, percent }) {
  return (
    <div>
      <div className="flex justify-between text-gray-600">
        <span>{label}</span>
        <span>{percent}%</span>
      </div>
      <div className="mt-1 h-2 w-full rounded-full bg-gray-100">
        <div className="h-2 rounded-full bg-[#3199CC]" style={{ width: percent + "%" }}></div>
      </div>
    </div>
  );
}
