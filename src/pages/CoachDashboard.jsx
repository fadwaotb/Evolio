import { useNavigate } from "react-router-dom";
import {
  Sidebar,
  coachLinks,
  Card,
  Button,
  Badge,
  StatCard,
} from "../components/Components.jsx";
import { students, reviews } from "../data.js";

// Career Coach Dashboard - review queue + workload summary.
export default function CoachDashboard() {
  const navigate = useNavigate();

  // Students waiting in the review queue (mock - just use all students)
  const reviewQueue = students;

  // Count reviews by status for the analytics row
  const needsRevision = reviews.filter((r) => r.status === "Needs Revision").length;
  const ready = reviews.filter((r) => r.status === "Ready").length;

  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Career Coach" links={coachLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Coach Dashboard</h1>

        {/* Workload summary */}
        <div className="mb-6 grid gap-4 sm:grid-cols-4">
          <StatCard label="In Queue" value={reviewQueue.length} />
          <StatCard label="Needs Revision" value={needsRevision} accent="teal" />
          <StatCard label="Ready" value={ready} />
          <StatCard label="Reviews Done" value={47} accent="teal" />
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Review queue */}
          <Card>
            <h3 className="mb-4 font-semibold text-gray-800">Review Queue</h3>
            <div className="space-y-3">
              {reviewQueue.map((student) => (
                <div
                  key={student.id}
                  className="flex items-center justify-between rounded-lg border border-gray-100 p-3"
                >
                  <div>
                    <p className="font-medium text-gray-800">{student.name}</p>
                    <p className="text-xs text-gray-500">{student.headline}</p>
                  </div>
                  <Button onClick={() => navigate(`/coach/review/${student.id}`)}>Review</Button>
                </div>
              ))}
            </div>
          </Card>

          {/* Recent feedback activity */}
          <Card>
            <h3 className="mb-4 font-semibold text-gray-800">Recent Feedback Activity</h3>
            <div className="space-y-3">
              {reviews.map((r) => (
                <div key={r.id} className="border-l-2 border-[#199DB2]/30 pl-3">
                  <div className="flex items-center gap-2">
                    <Badge text={r.status} color="teal" />
                    <span className="text-xs text-gray-400">{r.date}</span>
                  </div>
                  <p className="text-sm text-gray-500">{r.comment}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
