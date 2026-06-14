You are a professional Backend Engineer specializing in FastAPI, Python, clean backend architecture, and frontend-backend integration.

I already have the Evolio frontend. I want you to create a limited FastAPI backend and connect it to the existing frontend.

Important: this backend is only for the student portfolio workflow, plus login/create account for students and employers.

Do NOT build the full platform backend.
Do NOT build admin backend.
Do NOT build career coach/trainer backend.
Do NOT build employer management backend.
Do NOT create database tables yet.
Do NOT create SQLAlchemy models yet.
Do NOT create migrations.
Do NOT over-engineer the project.

I will create the SQLite database schema/tables in the next step. For now, only prepare the backend folder structure, Pydantic schemas, auth utilities, routers, file upload handling, API route structure, and frontend connection.

---

# Backend Scope

Build backend support only for these features:

1. Login
   - Students only
   - Employers only
   - No admin login
   - No career coach/trainer login

2. Create Account
   - Students only
   - Employers only
   - No admin registration
   - No career coach/trainer registration

3. Student Profile Editor
   - Student can create, read, and update their own profile
   - Fields:
     - name
     - headline
     - bio
     - skills
     - location
     - social links
     - contact email
     - portfolio availability status

4. Resume Upload
   - Upload resume
   - Replace resume
   - Preview/view resume metadata
   - Download resume
   - Delete resume
   - Store files locally for now

5. Project Pages
   - Create project
   - Get all student projects
   - Get single project
   - Update project
   - Delete project
   - Fields:
     - title
     - summary
     - description
     - rich text / Markdown content
     - tech stack
     - GitHub link
     - demo link
     - status
     - featured status
     - collaborators placeholder list

6. Save Rich Text / Markdown Editor Data
   - Save editor content as string data
   - Support Markdown/Rich Text content
   - Do not add advanced sanitization yet, but keep the structure ready for validation later

7. Upload Project Images
   - Upload screenshots/images
   - Get images for a project
   - Delete images
   - Store files locally for now
   - Return file path/URL to frontend

8. Shareable Work / Portfolio Links
   - Generate shareable portfolio link
   - Use token-style URL
   - Support visibility setting placeholder
   - Support optional expiration date placeholder
   - Employers can view shared portfolio data through the token
   - Do not build advanced permissions yet

9. Review Workflow
   - Student can submit portfolio for review
   - Student can view review status
   - Student can view mocked reviewer feedback
   - Review statuses:
     - Draft
     - Needs Revision
     - Ready
     - Published

---

# Required Backend Folder Structure

Create a backend folder with this structure:

backend/
main.py
requirements.txt
schemas.py
auth/
init.py
auth.py
routers/
init.py
auth_routes.py
profile.py
resume.py
project.py
image.py
share.py
review.py
db/
init.py
database.py

You may add only small utility files if necessary. Do not create too many files.

---

# Database Requirement for This Phase

I will use SQLite later.

For now:

- Prepare the db folder.
- Prepare a simple database.py placeholder if needed.
- Do not create real database tables.
- Do not create SQLAlchemy models.
- Do not create migrations.
- Use temporary in-memory data or JSON-style placeholders only if needed.
- Keep the code easy to connect to SQLite later.

---

# API Endpoints

Create REST endpoints under /api.

Auth:

- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

Profile:

- GET /api/profile
- PUT /api/profile

Resume:

- POST /api/resume/upload
- GET /api/resume
- GET /api/resume/download
- DELETE /api/resume

Projects:

- GET /api/projects
- GET /api/projects/{project_id}
- POST/api/projects
- PUT /api/projects/{project_id}
- DELETE /api/projects/{project_id}
- PUT /api/projects/{project_id}/content

Project Images:

- POST /api/projects/{project_id}/images
- GET /api/projects/{project_id}/images
- DELETE /api/projects/{project_id}/images/{image_id}

Share Links:

- POST /api/share/generate
- GET /api/share/{token}
- PUT /api/share/settings

Review Workflow:

- POST /api/review/submit
- GET /api/review/status
- GET /api/review/feedback

Health Check:

- GET /api/health

---

# Authentication Requirements

Use a simple JWT-style authentication structure.

For this phase, authentication can be mocked or in-memory, but the code should be structured so it can later connect to SQLite.

Rules:

- Students can manage only their own profile, resume, projects, images, share links, and review submission.
- Employers can register/login and view shared portfolio data only.
- Do not add admin permissions.
- Do not add career coach/trainer permissions.
- Store token in localStorage on the frontend for now if needed.

---

# File Upload Requirements

Use local file storage for now.

Create folders:

- `backend/uploads/resumes/`
- `backend/uploads/project_images/`

Allowed resume file types:

- PDF
- DOCX if simple to support

Allowed image file types:

- PNG
- JPG/JPEG

Add basic validation:

- File type check
- Max file size constant
- Safe filename handling
- Useful error messages

Return metadata to frontend:

- filename
- original filename
- file path or URL
- upload date
- file type
- file size

---

# Frontend Integration Requirements

Connect the existing React frontend pages to this backend.

Use browser fetch() only.

Do NOT use Axios.
Do NOT install Axios.

Create or update this helper file if needed:

src/services/api.js

The helper should use a centralized API base URL:

const API_BASE_URL = "http://localhost:8000/api";

Include functions like:

- registerUser(data)
- loginUser(data)
- getCurrentUser()
- getProfile()
- updateProfile(data)
- uploadResume(file)
- getResume()
- downloadResume()
- deleteResume()
- getProjects()
- getProject(id)
- createProject(data)
- updateProject(id, data)
- deleteProject(id)
- saveProjectContent(id, content)
- uploadProjectImage(projectId, file)
- getProjectImages(projectId)
- deleteProjectImage(projectId, imageId)
- generateShareLink(data)
- getPublicPortfolio(token)
- updateShareSettings(data)
- submitReview()
- getReviewStatus()
- getReviewFeedback()

Use FormData for file uploads.

Add token handling where needed:

- Save token after login
- Attach token to protected requests using Authorization header
- Handle basic unauthorized errors in the frontend

---

# CORS Requirements

Configure CORS in FastAPI so the React frontend can connect.

Allow local development origins:

- http://localhost:5173
- http://127.0.0.1:5173

---

# main.py Requirements

In main.py:

- Create FastAPI app
- Add CORS middleware
- Include all routers
- Add GET /api/health
- Serve uploaded files statically if needed
- Keep the file clean and easy to understand

---

# Requirements.txt

Include only necessary packages, such as:

- fastapi
- uvicorn
- python-multipart
- pydantic
- passlib[bcrypt]
- python-jose[cryptography]

Do not add unnecessary packages.

---

# Code Quality Requirements

Write clean, beginner-friendly code.

Use clear comments where helpful.

Keep the backend simple and understandable.

Do not add Docker.
Do not add tests unless I ask later.
Do not add production deployment setup.
Do not add unnecessary abstractions.
Do not build features outside the required scope.

---

# Run Commands

The backend should be runnable with:

pip install -r requirements.txt
uvicorn main:app --reload

If the command needs to be run from inside the backend folder, explain that clearly.

---

# Final Output Requirements

At the end, provide:

1. Backend folder structure
2. List of all created endpoints
3. How to run the FastAPI backend
4. How the frontend connects to the backend
5. Any frontend files changed
6. What is mocked/in-memory for now
7. What should be connected to SQLite in the next step
8. Any limitations or assumptions

Remember: build only the backend for the listed student portfolio features, plus student/employer login and create account. No admin backend, no career coach/trainer backend, no full platform backend, and no database tables yet.
