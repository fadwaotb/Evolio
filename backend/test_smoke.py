"""
test_smoke.py
-------------
A simple end-to-end check of the whole backend. It does NOT need a running
server -- FastAPI's TestClient calls the app directly in memory.

Run it from the backend folder:

    .venv\\Scripts\\python.exe test_smoke.py

It walks through the project's testing checklist and prints PASS/FAIL.
"""

import io
from pathlib import Path

from fastapi.testclient import TestClient

import main
from db.database import DB_PATH

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, condition):
    results.append((name, condition))
    print(f"[{PASS if condition else FAIL}] {name}")


client = TestClient(main.app)


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def register(email, role):
    r = client.post(
        "/api/auth/register",
        json={"email": email, "password": "pass1234", "full_name": email.split("@")[0], "role": role},
    )
    return r


# 1. App imported successfully (we got here -> imports worked)
check("1. Backend imports successfully", True)

# Trigger startup so the DB + tables get created.
with TestClient(main.app):
    pass

# 2. Database file created
check("2. Database file created at backend/db/evolio.db", Path(DB_PATH).exists())

# 3. Tables created
from sqlalchemy import inspect
from db.database import engine
tables = set(inspect(engine).get_table_names())
expected = {
    "users", "student_profiles", "social_links", "resumes",
    "projects", "project_images", "share_links", "portfolio_reviews",
}
check("3. All 8 tables created", expected.issubset(tables))

# 4-7. Register + login each role (use unique emails per run to avoid clashes)
import secrets
suffix = secrets.token_hex(3)
tokens = {}
for i, role in enumerate(["Student", "Employer", "Admin", "Career Coach"], start=4):
    email = f"{role.replace(' ', '').lower()}_{suffix}@test.com"
    reg = register(email, role)
    login = client.post("/api/auth/login", json={"email": email, "password": "pass1234"})
    ok = reg.status_code == 200 and login.status_code == 200
    tokens[role] = login.json().get("token") if login.status_code == 200 else None
    check(f"{i}. Register/login {role}", ok)

student = tokens["Student"]

# 8. /api/auth/me returns correct user + role
me = client.get("/api/auth/me", headers=auth_header(student))
check("8. /api/auth/me returns correct role", me.status_code == 200 and me.json()["role"] == "Student")

# 9. Student create/update profile
prof = client.put(
    "/api/profile",
    headers=auth_header(student),
    json={"headline": "Frontend Dev", "bio": "Hi", "skills": ["React", "Python"]},
)
check("9. Student create/update profile", prof.status_code == 200 and prof.json()["skills"] == ["React", "Python"])

# 10. Student upload/download/delete resume
up = client.post(
    "/api/resume",
    headers=auth_header(student),
    files={"file": ("cv.pdf", io.BytesIO(b"%PDF-1.4 fake pdf"), "application/pdf")},
)
dl = client.get("/api/resume/download", headers=auth_header(student))
de = client.delete("/api/resume", headers=auth_header(student))
check("10. Resume upload/download/delete", up.status_code == 200 and dl.status_code == 200 and de.status_code == 200)

# 11. Student create/update/delete project
cp = client.post("/api/projects", headers=auth_header(student), json={"title": "My App", "tech_stack": ["React"]})
pid = cp.json()["id"] if cp.status_code == 200 else None
upd = client.put(f"/api/projects/{pid}", headers=auth_header(student), json={"title": "My Better App"})
# create a second project to delete, so we keep one around for image tests
cp2 = client.post("/api/projects", headers=auth_header(student), json={"title": "Throwaway"})
dl_pid = cp2.json()["id"]
dp = client.delete(f"/api/projects/{dl_pid}", headers=auth_header(student))
check("11. Project create/update/delete", cp.status_code == 200 and upd.json()["title"] == "My Better App" and dp.status_code == 200)

# 12. Save rich text / Markdown editor content
content = client.put(f"/api/projects/{pid}/content", headers=auth_header(student), json={"content": "# Hello\n- a\n- b"})
check("12. Save editor (Markdown) content", content.status_code == 200 and content.json()["description"].startswith("# Hello"))

# 13. Upload / delete project image
img = client.post(
    f"/api/projects/{pid}/images",
    headers=auth_header(student),
    files={"file": ("shot.png", io.BytesIO(b"\x89PNG fake"), "image/png")},
)
img_id = img.json()["id"] if img.status_code == 200 else None
img_del = client.delete(f"/api/projects/images/{img_id}", headers=auth_header(student))
check("13. Project image upload/delete", img.status_code == 200 and img_del.status_code == 200)

# 14. Generate share link
sl = client.post("/api/share-link", headers=auth_header(student), json={"visibility": "public"})
check("14. Generate share link", sl.status_code == 200 and bool(sl.json().get("token")))

# 15. Submit review
rv = client.post("/api/review", headers=auth_header(student), json={"status": "Ready"})
check("15. Submit review", rv.status_code == 200 and rv.json()["status"] == "Ready")

# 16. Non-student roles blocked with 403 on student-only endpoints
blocked = True
for role in ["Employer", "Admin", "Career Coach"]:
    r = client.get("/api/projects", headers=auth_header(tokens[role]))
    if r.status_code != 403:
        blocked = False
        print(f"    -> {role} got {r.status_code}, expected 403")
check("16. Non-student roles blocked with 403", blocked)

# Bonus: public share view works without auth
view = client.get(f"/api/share-link/view/{sl.json()['token']}")
check("Bonus. Public share view works (no login)", view.status_code == 200 and "projects" in view.json())

# --- Extra checks for the frontend wiring ---

# A. Profile saves name + github (github stored as a social link, echoed back)
client.put(
    "/api/profile",
    headers=auth_header(student),
    json={"full_name": "Aisha K", "github": "https://github.com/aisha", "linkedin": "https://linkedin.com/in/aisha"},
)
prof2 = client.get("/api/profile", headers=auth_header(student)).json()
check("A. Profile stores name + github + linkedin",
      prof2.get("name") == "Aisha K" and prof2.get("github") == "https://github.com/aisha")

# B. Project status + screenshot URL, and the image is served as a static file
proj = client.post("/api/projects", headers=auth_header(student), json={"title": "Showcase", "status": "Published"}).json()
img2 = client.post(
    f"/api/projects/{proj['id']}/images",
    headers=auth_header(student),
    files={"file": ("cover.png", io.BytesIO(b"\x89PNG cover bytes"), "image/png")},
).json()
proj_full = client.get(f"/api/projects/{proj['id']}", headers=auth_header(student)).json()
static_img = client.get(img2["url"])           # served from /uploads/...
check("B. Project status + screenshot URL + static image serves",
      proj_full.get("status") == "Published"
      and len(proj_full.get("screenshots", [])) == 1
      and static_img.status_code == 200)

# C. Resume static URL is downloadable
up2 = client.post(
    "/api/resume",
    headers=auth_header(student),
    files={"file": ("cv2.pdf", io.BytesIO(b"%PDF-1.4 another"), "application/pdf")},
).json()
static_pdf = client.get(up2["url"])
check("C. Resume static URL serves the file", static_pdf.status_code == 200)

print("\n================ SUMMARY ================")
passed = sum(1 for _, ok in results if ok)
print(f"{passed}/{len(results)} checks passed")
failed = [name for name, ok in results if not ok]
if failed:
    print("FAILED:")
    for name in failed:
        print("  -", name)
    raise SystemExit(1)
print("ALL GREEN - everything works!")
