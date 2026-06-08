import {
  Sidebar,
  adminLinks,
  Card,
  Button,
  Badge,
  StatCard,
} from "../components/Components.jsx";
import { coaches } from "../data.js";

// Career Coach Management Page - admin views coaches and their performance.
export default function CoachManagementPage() {
  // Add up totals for the summary cards
  const totalStudents = coaches.reduce((sum, c) => sum + c.assignedStudents, 0);
  const totalReviews = coaches.reduce((sum, c) => sum + c.reviewsCompleted, 0);

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Admin" links={adminLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Coach Management</h1>

        {/* Performance summary */}
        <div className="mb-6 grid gap-4 sm:grid-cols-3">
          <StatCard label="Total Coaches" value={coaches.length} />
          <StatCard label="Students Assigned" value={totalStudents} accent="teal" />
          <StatCard label="Reviews Completed" value={totalReviews} />
        </div>

        {/* Coach directory */}
        <Card>
          <h3 className="mb-4 font-semibold text-gray-800">Coach Directory</h3>
          <div className="space-y-3">
            {coaches.map((coach) => (
              <div
                key={coach.id}
                className="flex flex-col gap-2 rounded-lg border border-gray-100 p-3 sm:flex-row sm:items-center sm:justify-between"
              >
                <div>
                  <p className="font-medium text-gray-800">{coach.name}</p>
                  <p className="text-xs text-gray-500">{coach.email}</p>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Badge text={`${coach.assignedStudents} students`} color="blue" />
                  <Badge text={`${coach.reviewsCompleted} reviews`} color="teal" />
                  <Badge text={`★ ${coach.rating}`} color="yellow" />
                  {/* Assignment management (mock) */}
                  <Button variant="outline">Assign Students</Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </main>
    </div>
  );
}
