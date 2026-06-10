import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Navbar, Card, Input, Button } from "../components/Components.jsx";
import { loginUser, setToken } from "../services/api.js";

// Sign In Page - logs in against the backend and stores the auth token.
export default function SignInPage() {
  const navigate = useNavigate();

  // Simple form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Student");
  const [error, setError] = useState("");

  // All four account types can sign in.
  const roles = ["Student", "Employer", "Career Coach", "Admin"];

  // Handle the login button - calls the backend, saves the token, redirects.
  async function handleLogin(e) {
    e.preventDefault();

    // Very basic validation
    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }
    setError("");

    try {
      const data = await loginUser({ email, password, role });
      setToken(data.access_token);

      // Send the user to the right dashboard based on their role.
      if (data.role === "student") navigate("/student/dashboard");
      else if (data.role === "employer") navigate("/employer/dashboard");
      else if (data.role === "coach") navigate("/coach/dashboard");
      else if (data.role === "admin") navigate("/admin/dashboard");
    } catch (err) {
      setError(err.message || "Login failed. Please try again.");
    }
  }

  return (
    <div>
      <Navbar />

      <div className="auth-container">
        <h1 className="auth-title">Sign In to Evolio</h1>

        <Card>
          <form onSubmit={handleLogin}>
            {/* Show an error message if validation fails */}
            {error && <p className="alert-error">{error}</p>}

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
              <label className="form-label">I am a...</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="form-input"
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
