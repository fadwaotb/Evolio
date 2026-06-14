// =============================================================
// api.js
// One small place that talks to the FastAPI backend.
// Every page imports the functions it needs from here, so the
// pages stay clean and we never repeat fetch() code.
// =============================================================

// Where the backend is running (uvicorn main:app --reload).
// If you deploy later, change this one line.
export const API_BASE = "http://127.0.0.1:8000";

// ---- Token storage (so the user stays logged in after refresh) ----
const TOKEN_KEY = "evolio_token";
const USER_KEY = "evolio_user";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}
export function getUser() {
  const raw = localStorage.getItem(USER_KEY);
  return raw ? JSON.parse(raw) : null;
}
export function saveAuth(token, user) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}
export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

// Turn a backend path like "/uploads/x.png" into a full URL the browser can load.
export function fileUrl(path) {
  if (!path) return "";
  if (path.startsWith("http")) return path;
  return API_BASE + path;
}

// ---- The core request helper ----
// - Adds the Authorization header automatically when logged in.
// - Sends JSON for normal calls; sends FormData as-is for file uploads.
// - Throws an Error with the backend's message when something fails.
async function request(path, { method = "GET", body, isForm = false } = {}) {
  const headers = {};
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  let payload = body;
  if (body && !isForm) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  const res = await fetch(API_BASE + path, { method, headers, body: payload });

  // 204 No Content or empty body
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const message = (data && data.detail) || `Request failed (${res.status})`;
    throw new Error(message);
  }
  return data;
}

// ===================== AUTH =====================
export async function register({ email, password, full_name, role }) {
  const data = await request("/api/auth/register", {
    method: "POST",
    body: { email, password, full_name, role },
  });
  saveAuth(data.token, data.user);
  return data;
}

export async function login({ email, password }) {
  const data = await request("/api/auth/login", {
    method: "POST",
    body: { email, password },
  });
  saveAuth(data.token, data.user);
  return data;
}

export function getMe() {
  return request("/api/auth/me");
}

// ===================== PROFILE =====================
export function getProfile() {
  return request("/api/profile");
}
export function saveProfile(profile) {
  return request("/api/profile", { method: "PUT", body: profile });
}

// ===================== RESUME =====================
export function getResume() {
  return request("/api/resume");
}
export function uploadResume(file) {
  const form = new FormData();
  form.append("file", file);
  return request("/api/resume", { method: "POST", body: form, isForm: true });
}
export function deleteResume() {
  return request("/api/resume", { method: "DELETE" });
}

// ===================== PROJECTS =====================
export function listProjects() {
  return request("/api/projects");
}
export function getProject(id) {
  return request(`/api/projects/${id}`);
}
export function createProject(project) {
  return request("/api/projects", { method: "POST", body: project });
}
export function updateProject(id, project) {
  return request(`/api/projects/${id}`, { method: "PUT", body: project });
}
export function deleteProject(id) {
  return request(`/api/projects/${id}`, { method: "DELETE" });
}
export function uploadProjectImage(projectId, file) {
  const form = new FormData();
  form.append("file", file);
  return request(`/api/projects/${projectId}/images`, {
    method: "POST",
    body: form,
    isForm: true,
  });
}

// ===================== SHARE LINK =====================
export function getShareLink() {
  return request("/api/share-link");
}
export function createShareLink(visibility = "public") {
  return request("/api/share-link", { method: "POST", body: { visibility } });
}

// ===================== REVIEW =====================
export function getReview() {
  return request("/api/review");
}
export function submitReview(status, feedback) {
  return request("/api/review", { method: "POST", body: { status, feedback } });
}
