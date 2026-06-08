import { Link } from "react-router-dom";
import {
  Sidebar,
  studentLinks,
  StatCard,
  Card,
  Button,
  AIBox,
  Badge,
} from "../components/Components.jsx";
import { analytics } from "../data.js";

// Student Dashboard - overview of the student's progress and stats.
export default function StudentDashboard() {
  // Grab the student numbers from our mock data
  const stats = analytics.student;

  // Simple mock recent activity list
  const recentActivity = [
    { text: "Coach left feedback on your portfolio", time: "2h ago" },
    { text: "Your Weather Dashboard project got 5 new views", time: "1d ago" },
    { text: "An employer downloaded your resume", time: "2d ago" },
  ];

  return (
    <div className="flex flex-col md:flex-row">
      {/* Left menu */}
      <Sidebar title="Student" links={studentLinks} />

      {/* Main content */}
      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Dashboard</h1>

        {/* Status row */}
        <div className="mb-6 grid gap-4 sm:grid-cols-3">
          <Card>
            <p className="text-sm text-gray-500">Profile Completion</p>
            <p className="mt-1 text-2xl font-bold text-blue-600">{stats.profileCompletion}%</p>
            {/* Simple progress bar */}
            <div className="mt-2 h-2 w-full rounded-full bg-gray-100">
              <div
                className="h-2 rounded-full bg-teal-500"
                style={{ width: stats.profileCompletion + "%" }}
              ></div>
            </div>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Resume Status</p>
            <div className="mt-2">
              <Badge text={stats.resumeStatus} color="green" />
            </div>
          </Card>
          <Card>
            <p className="text-sm text-gray-500">Review Status</p>
            <div className="mt-2">
              <Badge text={stats.reviewStatus} color="yellow" />
            </div>
          </Card>
        </div>

        {/* Numbers grid */}
        <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          <StatCard label="Projects" value={stats.projectCount} />
          <StatCard label="Portfolio Views" value={stats.portfolioViews} accent="teal" />
          <StatCard label="Project Views" value={stats.projectViews} />
          <StatCard label="Resume Downloads" value={stats.resumeDownloads} accent="teal" />
          <StatCard label="GitHub Clicks" value={stats.githubClicks} />
          <StatCard label="Demo Clicks" value={stats.demoClicks} accent="teal" />
        </div>

        {/* Quick links */}
        <div className="mb-6 flex flex-wrap gap-3">
          <Link to="/student/profile">
            <Button>Edit Profile</Button>
          </Link>
          <Link to="/student/projects">
            <Button variant="outline">Manage Projects</Button>
          </Link>
          <Link to="/student/review">
            <Button variant="teal">Submit for Review</Button>
          </Link>
        </div>

        {/* Recent activity (simple mock list) */}
        <Card className="mb-6">
          <h3 className="mb-4 font-semibold text-gray-800">Recent Activity</h3>
          <div className="space-y-3 text-sm">
            {recentActivity.map((item, index) => (
              <div key={index} className="flex justify-between border-b border-gray-100 pb-2">
                <span className="text-gray-600">{item.text}</span>
                <span className="text-gray-400">{item.time}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* AI readiness summary (fake AI) */}
        <AIBox
          title="AI Readiness Summary"
          buttonLabel="Check My Readiness"
          result="You're 85% job ready! Finish your profile and publish 1 more project to reach 100%."
        />
      </main>
    </div>
  );
}
