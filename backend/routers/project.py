"""
Project routes: create, list, get, update, delete, and save editor content.

Each student only sees and manages their own projects.
"""

from fastapi import APIRouter, Depends, HTTPException

from auth.auth import require_student
from db.database import next_id, projects
from schemas import ProjectContentIn, ProjectIn, ProjectOut

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _get_owned_project(project_id: int, user) -> dict:
    """Fetch a project and make sure it belongs to the current student."""
    project = projects.get(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    if project["owner_id"] != user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own projects.",
        )
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects(user=Depends(require_student)):
    mine = [p for p in projects.values() if p["owner_id"] == user["id"]]
    return [ProjectOut(**p) for p in mine]


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(project_id: int, user=Depends(require_student)):
    return ProjectOut(**_get_owned_project(project_id, user))


@router.post("", response_model=ProjectOut)
def create_project(data: ProjectIn, user=Depends(require_student)):
    project_id = next_id()
    project = data.model_dump()
    project["id"] = project_id
    project["owner_id"] = user["id"]
    projects[project_id] = project
    return ProjectOut(**project)


@router.put("/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, data: ProjectIn, user=Depends(require_student)):
    existing = _get_owned_project(project_id, user)
    updated = data.model_dump()
    updated["id"] = existing["id"]
    updated["owner_id"] = existing["owner_id"]
    projects[project_id] = updated
    return ProjectOut(**updated)


@router.delete("/{project_id}")
def delete_project(project_id: int, user=Depends(require_student)):
    _get_owned_project(project_id, user)
    projects.pop(project_id, None)
    return {"message": "Project deleted."}


@router.put("/{project_id}/content", response_model=ProjectOut)
def save_project_content(
    project_id: int, data: ProjectContentIn, user=Depends(require_student)
):
    """Save the rich text / Markdown editor content for a project."""
    project = _get_owned_project(project_id, user)
    # No advanced sanitization yet -- just store the string.
    project["content"] = data.content
    projects[project_id] = project
    return ProjectOut(**project)
