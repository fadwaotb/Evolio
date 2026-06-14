import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Navbar, Card, Input, Button } from "../components/Components.jsx";
import { login } from "../api.js";

// Where each role lands after a successful login.
const dashboardFor = {
  Student: "/student/dashboard",
  Employer: "/employer/dashboard",
  "Career Coach": "/coach/dashboard",
  Admin: "/admin/dashboard",
};

// Sign In Page - real login against the backend.
export default function SignInPage() {
  const navigate = useNavigate();

  // Simple form state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Handle the login button (real auth via the API)
  async function handleLogin(e) {
    e.preventDefault();

    // Very basic validation
    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }
    setError("");
    setLoading(true);

    try {
      // The backend tells us the real role from the account itself.
      const { user } = await login({ email, password });
      navigate(dashboardFor[user.role] || "/");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
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

            <Button type="submit">{loading ? "Signing in..." : "Sign In"}</Button>
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
