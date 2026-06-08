import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Navbar, Card, Input, Button } from "../components/Components.jsx";

// Sign In Page - mock login that redirects based on the chosen role.
export default function SignInPage() {
  const navigate = useNavigate();

  // Simple form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Student");
  const [error, setError] = useState("");

  // The 4 roles a user can log in as
  const roles = ["Student", "Employer", "Career Coach", "Admin"];

  // Handle the login button (no real auth - just redirect)
  function handleLogin(e) {
    e.preventDefault();

    // Very basic validation
    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }
    setError("");

    // Send the user to the right dashboard based on their role
    if (role === "Student") navigate("/student/dashboard");
    if (role === "Employer") navigate("/employer/dashboard");
    if (role === "Career Coach") navigate("/coach/dashboard");
    if (role === "Admin") navigate("/admin/dashboard");
  }

  return (
    <div>
      <Navbar />

      <div className="mx-auto max-w-md px-6 py-12">
        <h1 className="mb-6 text-center text-2xl font-bold text-gray-800">Sign In to Evolio</h1>

        <Card>
          <form onSubmit={handleLogin}>
            {/* Show an error message if validation fails */}
            {error && (
              <p className="mb-4 rounded-lg bg-red-50 p-2 text-sm text-red-600">{error}</p>
            )}

            <Input
              label="Email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="you@example.com"
            />
            <Input
              label="Password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
            />

            {/* Role selector */}
            <div className="mb-4">
              <label className="mb-1 block text-sm font-medium text-gray-700">I am a...</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-[#3199CC] focus:outline-none"
              >
                {roles.map((r) => (
                  <option key={r}>{r}</option>
                ))}
              </select>
            </div>

            <Button type="submit">Sign In</Button>
          </form>
        </Card>

        <p className="mt-4 text-center text-sm text-gray-500">
          No account?{" "}
          <Link to="/create-account" className="text-[#001776] hover:underline">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
