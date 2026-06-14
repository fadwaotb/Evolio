"""
seed_data.py
------------
Fills the database with the project's suggested SAMPLE dataset:

    10 students   20 projects   5 resumes   10 images   5 reviews

Run it from the backend folder:

    .venv\\Scripts\\python.exe seed_data.py

WARNING: this WIPES the existing data first, then inserts the fresh sample set,
so you always get the same known data. Real files for resumes (.pdf) and
project images (.svg) are written under backend/uploads/.
"""

import secrets
from datetime import datetime, timedelta
from pathlib import Path

import auth_utils
import storage
from db import model, repository
from db.database import SessionLocal, init_db


# ---------------------------------------------------------------------------
# Small helpers to build REAL placeholder files
# ---------------------------------------------------------------------------
def make_pdf(text: str) -> bytes:
    """Build a tiny but VALID one-page PDF that shows `text`."""
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
    ]
    stream = f"BT /F1 22 Tf 72 700 Td ({text}) Tj ET".encode("latin-1")
    objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    pdf = b"%PDF-1.4\n"
    offsets = []
    for i, obj in enumerate(objects, start=1):
        offsets.append(len(pdf))
        pdf += str(i).encode() + b" 0 obj\n" + obj + b"\nendobj\n"

    xref_pos = len(pdf)
    n = len(objects) + 1
    pdf += b"xref\n0 " + str(n).encode() + b"\n0000000000 65535 f \n"
    for off in offsets:
        pdf += ("%010d 00000 n \n" % off).encode()
    pdf += b"trailer\n<< /Size " + str(n).encode() + b" /Root 1 0 R >>\n"
    pdf += b"startxref\n" + str(xref_pos).encode() + b"\n%%EOF"
    return pdf


def make_svg(label: str, color: str) -> bytes:
    """A colorful SVG placeholder image (renders in the browser as <img>)."""
    svg = (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='750'>"
        f"<rect width='100%' height='100%' fill='{color}'/>"
        f"<text x='50%' y='50%' font-family='Arial, sans-serif' font-size='52' "
        f"fill='white' font-weight='bold' text-anchor='middle' "
        f"dominant-baseline='middle'>{label}</text></svg>"
    )
    return svg.encode("utf-8")


def write_file(target_dir: Path, original_name: str, data: bytes, content_type: str) -> dict:
    """Write bytes to disk and return the metadata dict the repository expects."""
    target_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{secrets.token_hex(8)}{Path(original_name).suffix}"
    file_path = target_dir / stored_name
    file_path.write_bytes(data)
    return {
        "original_name": original_name,
        "stored_name": stored_name,
        "file_path": str(file_path),
        "content_type": content_type,
        "size_bytes": len(data),
    }


# ---------------------------------------------------------------------------
# The sample data
# ---------------------------------------------------------------------------
STUDENTS = [
    ("Aisha Khan",      "Frontend Developer | React Enthusiast", "Austin, TX",   ["React", "JavaScript", "Tailwind CSS"]),
    ("Marcus Lee",      "Full Stack Developer",                  "Seattle, WA",  ["Node.js", "React", "MongoDB"]),
    ("Priya Patel",     "Junior Software Engineer",              "Remote",       ["Python", "Django", "SQL"]),
    ("David Chen",      "Data Analyst",                          "New York, NY", ["Python", "Pandas", "Power BI"]),
    ("Sara Johnson",    "Machine Learning Engineer",             "Boston, MA",   ["Python", "TensorFlow", "scikit-learn"]),
    ("Omar Farouk",     "Backend Developer",                     "Chicago, IL",  ["FastAPI", "PostgreSQL", "Docker"]),
    ("Lena Müller",     "UI/UX Designer & Developer",            "Remote",       ["Figma", "React", "CSS"]),
    ("Carlos Gomez",    "DevOps Engineer",                       "Miami, FL",    ["AWS", "Kubernetes", "Terraform"]),
    ("Yuki Tanaka",     "Mobile Developer",                      "San Jose, CA", ["React Native", "TypeScript", "Firebase"]),
    ("Fatima Al-Sayed", "Data Scientist",                        "Remote",       ["Python", "SQL", "Tableau"]),
]

COLORS = ["#001776", "#199DB2", "#3199CC", "#0F766E", "#7C3AED", "#DB2777", "#EA580C", "#16A34A"]

PROJECT_TITLES = [
    "Weather Dashboard", "Task Manager API", "E-commerce Store", "Portfolio Website",
    "Movie Recommender", "Chat Application", "Expense Tracker", "Blog Platform",
    "Fitness Tracker", "Recipe Finder", "Job Board", "Quiz App",
    "Inventory System", "Social Feed", "URL Shortener", "Music Player",
    "Notes App", "Crypto Tracker", "Booking System", "Survey Tool",
]

TECH_POOL = [
    ["React", "Vite", "Tailwind"], ["FastAPI", "PostgreSQL"], ["Node.js", "Express", "MongoDB"],
    ["Python", "Pandas"], ["Django", "SQLite"], ["React Native", "Firebase"],
]

REVIEW_PLAN = [
    ("Published",      "Great work! Your portfolio is polished and ready to share."),
    ("Ready",          "Looks good. Submitted for a final coach review."),
    ("Needs Revision", "Add more detail to your project descriptions and a demo link."),
    ("Draft",          "Still a work in progress."),
    ("Ready",          "Strong projects. One small typo on the profile bio."),
]


def wipe(db):
    """Delete all existing rows + uploaded files for a clean, repeatable seed."""
    for m in [
        model.PortfolioReview, model.ProjectImage, model.Project,
        model.SocialLink, model.Resume, model.StudentProfile,
        model.ShareLink, model.User,
    ]:
        db.query(m).delete()
    db.commit()

    for folder in [storage.RESUMES_DIR, storage.PROJECT_IMAGES_DIR]:
        if folder.exists():
            for f in folder.iterdir():
                if f.name != ".gitkeep":
                    f.unlink()


def run():
    init_db()
    storage.ensure_upload_dirs()
    db = SessionLocal()
    try:
        wipe(db)

        # --- 10 students (User + StudentProfile + github/linkedin links) ---
        users = []
        for i, (name, headline, location, skills) in enumerate(STUDENTS):
            email = f"student{i + 1}@evolio.com"
            user = repository.create_user(
                db,
                email=email,
                password_hash=auth_utils.hash_password("pass1234"),
                full_name=name,
                role="Student",
            )
            handle = name.split()[0].lower()
            repository.create_or_update_profile(db, user.id, {
                "headline": headline,
                "bio": f"Bootcamp graduate. {headline}. Passionate about building real projects.",
                "location": location,
                "skills": skills,
                "availability": ["Open to work", "Interviewing", "Not looking"][i % 3],
                "contact_email": email,
                "avatar_color": COLORS[i % len(COLORS)],
            })
            profile = repository.get_profile_by_user_id(db, user.id)
            repository.upsert_social_link_by_type(db, profile.id, "GitHub", f"https://github.com/{handle}")
            repository.upsert_social_link_by_type(db, profile.id, "LinkedIn", f"https://linkedin.com/in/{handle}")
            users.append(user)

        # --- 20 projects (2 per student) ---
        projects = []
        for idx, title in enumerate(PROJECT_TITLES):
            owner = users[idx // 2]            # students 0..9, two projects each
            tech = TECH_POOL[idx % len(TECH_POOL)]
            project = repository.create_project(db, owner.id, {
                "title": title,
                "summary": f"A {title.lower()} built during the bootcamp.",
                "description": (
                    f"# {title}\n\n"
                    f"**Overview:** {title} solving a real-world problem.\n\n"
                    f"## Tools\n- " + "\n- ".join(tech) + "\n\n"
                    f"## Role\nDesigned and built the full {title.lower()} end to end."
                ),
                "tech_stack": tech,
                "status": "Published" if idx % 3 != 0 else "Draft",
                "is_featured": (idx % 5 == 0),     # a few featured
                "github_link": f"https://github.com/example/{title.lower().replace(' ', '-')}",
                "demo_link": f"https://demo.example.com/{title.lower().replace(' ', '-')}",
                "role": "Full Stack Developer",
                "duration": "3 weeks",
            })
            projects.append(project)

        # --- 5 resumes (for the first 5 students) ---
        for i in range(5):
            user = users[i]
            meta = write_file(
                storage.RESUMES_DIR,
                f"{STUDENTS[i][0].replace(' ', '_')}_Resume.pdf",
                make_pdf(f"{STUDENTS[i][0]} - Resume"),
                "application/pdf",
            )
            repository.save_resume_metadata(db, user.id, meta)

        # --- 10 images (one on each of the first 10 projects) ---
        for i in range(10):
            project = projects[i]
            meta = write_file(
                storage.PROJECT_IMAGES_DIR,
                f"{project.title.replace(' ', '_')}.svg",
                make_svg(project.title, COLORS[i % len(COLORS)]),
                "image/svg+xml",
            )
            repository.save_project_image_metadata(db, project.id, meta)

        # --- 5 reviews (for the first 5 students) ---
        base = datetime.utcnow()
        for i, (status, feedback) in enumerate(REVIEW_PLAN):
            review = repository.submit_review(db, users[i].id, status, feedback)
            review.submitted_at = base - timedelta(days=i)
            if status in ("Published", "Ready", "Needs Revision"):
                review.reviewed_at = base - timedelta(days=i) + timedelta(hours=3)
        db.commit()

        # --- Summary ---
        counts = {
            "students": db.query(model.User).count(),
            "profiles": db.query(model.StudentProfile).count(),
            "projects": db.query(model.Project).count(),
            "resumes": db.query(model.Resume).count(),
            "images": db.query(model.ProjectImage).count(),
            "reviews": db.query(model.PortfolioReview).count(),
            "social_links": db.query(model.SocialLink).count(),
        }
        print("Sample dataset created:")
        for k, v in counts.items():
            print(f"  {k:14}: {v}")
        print("\nLogin with any of:  student1@evolio.com ... student10@evolio.com")
        print("Password for all :  pass1234")
    finally:
        db.close()


if __name__ == "__main__":
    run()
