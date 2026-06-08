import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { Navbar, Card, Input, Button } from "../components/Components.jsx";

// Create Account Page - simple sign up form with basic validation.
export default function CreateAccountPage() {
  const navigate = useNavigate();

  // Form state
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [role, setRole] = useState("Student");
  const [agreed, setAgreed] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  const roles = ["Student", "Employer", "Career Coach", "Admin"];

  // Validate the form, then pretend to create the account.
  function handleSubmit(e) {
    e.preventDefault();

    // Simple validation checks
    if (!name || !email || !password) {
      setError("Please fill in all fields.");
      return;
    }
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }
    if (!agreed) {
      setError("Please accept the terms to continue.");
      return;
    }

    // All good - show success then redirect to sign in
    setError("");
    setSuccess(true);
    setTimeout(() => navigate("/sign-in"), 1200);
  }

  return (
    <div>
      <Navbar />

      <div className="mx-auto max-w-md px-6 py-12">
        <h1 className="mb-6 text-center text-2xl font-bold text-gray-800">Create Your Account</h1>

        <Card>
          {/* Success message after creating account */}
          {success ? (
            <p className="rounded-lg bg-green-50 p-3 text-center text-sm text-green-700">
              Account created! Redirecting to sign in...
            </p>
          ) : (
            <form onSubmit={handleSubmit}>
              {error && (
                <p className="mb-4 rounded-lg bg-red-50 p-2 text-sm text-red-600">{error}</p>
              )}

              <Input label="Full Name" value={name} onChange={(e) => setName(e.target.value)} />
              <Input
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
              <Input
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
              <Input
                label="Confirm Password"
                type="password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
              />

              {/* Role selector */}
              <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-gray-700">Role</label>
                <select
                  value={role}
                  onChange={(e) => setRole(e.target.value)}
                  className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none"
                >
                  {roles.map((r) => (
                    <option key={r}>{r}</option>
                  ))}
                </select>
              </div>

              {/* Terms checkbox */}
              <label className="mb-4 flex items-center gap-2 text-sm text-gray-600">
                <input
                  type="checkbox"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                />
                I agree to the Terms and Conditions
              </label>

              <Button type="submit">Create Account</Button>
            </form>
          )}
        </Card>

        <p className="mt-4 text-center text-sm text-gray-500">
          Already have an account?{" "}
          <Link to="/sign-in" className="text-blue-600 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
}
