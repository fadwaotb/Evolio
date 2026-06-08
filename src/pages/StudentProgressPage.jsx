import {
  Sidebar,
  coachLinks,
  Card,
  Badge,
  StatCard,
  AIBox,
} from "../components/Components.jsx";
import { students, reviews, aiFeedback } from "../data.js";

// Student Progress Page - the coach tracks student completion + history.
export default function StudentProgressPage() {
  return (
    <div className="flex flex-col md:flex-row">
      <Sidebar title="Career Coach" links={coachLinks} />

      <main className="flex-1 p-6">
        <h1 className="mb-6 text-2xl font-bold text-gray-800">Student Progress</h1>

        {/* Completion metrics for each student */}
        <div className="mb-6 grid gap-4 md:grid-cols-3">
          {students.map((student) => (
            <Card key={student.id}>
              <p className="font-medium text-gray-800">{student.name}</p>
              <p className="mb-2 text-xs text-gray-500">{student.headline}</p>

              {/* Progress bar for completion */}
              <p className="text-sm text-gray-500">Completion: {student.profileCompletion}%</p>
              <div className="mt-1 h-2 w-full rounded-full bg-gray-100">
                <div
                  className="h-2 rounded-full bg-teal-500"
                  style={{ width: student.profileCompletion + "%" }}
                ></div>
              </div>
            </Card>
          ))}
        </div>

        {/* Progress trend numbers */}
        <div className="mb-6 grid gap-4 sm:grid-cols-3">
          <StatCard label="Avg Completion" value="62%" />
          <StatCard label="Reviews This Month" value={reviews.length} accent="teal" />
          <StatCard label="Improving Students" value={2} />
        </div>

        <div className="grid gap-6 lg:grid-cols-2">
          {/* Review history */}
          <Card>
            <h3 className="mb-4 font-semibold text-gray-800">Review History</h3>
            <div className="space-y-3">
              {reviews.map((r) => (
                <div key={r.id} className="border-l-2 border-blue-200 pl-3">
                  <div className="flex items-center gap-2">
                    <Badge text={r.status} color="blue" />
                    <span className="text-xs text-gray-400">{r.date}</span>
                  </div>
                  <p className="text-sm text-gray-500">{r.comment}</p>
                </div>
              ))}
            </div>
          </Card>

          {/* AI coaching insights (fake) */}
          <AIBox
            title="AI Coaching Insights"
            buttonLabel="Get Insights"
            result="Most students need help adding demo links and writing stronger project descriptions. Consider a group workshop on portfolios."
          />
        </div>
      </main>
    </div>
  );
}
