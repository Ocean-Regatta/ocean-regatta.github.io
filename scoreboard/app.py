import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Header, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy import create_engine, func, desc, asc
from sqlalchemy.orm import sessionmaker, Session

from models import Base, Edition, Student, Run, Badge, StudentBadge

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./scoreboard.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        editions_data = [
            {
                "id": "2026",
                "year": 2026,
                "name": "Ocean Regatta 2026 (Chenal & Quai Sonar)",
                "is_active": True,
                "description": "Courant marin transversal, contournement de cardinale IALA et suivi de quai au sonar Ping2.",
                "template_url": "https://github.com/ocean-regatta/ocean-regatta-2026-template"
            }
        ]
        for ed in editions_data:
            existing = db.query(Edition).filter(Edition.id == ed["id"]).first()
            if not existing:
                db.add(Edition(**ed))

        badges_data = [
            Badge(id="SPEED_DEMON", title="Speed Demon", description="Record absolu de rapidit? sur le parcours valid?.", icon="?", is_exclusive=True),
            Badge(id="SEA_TURTLE", title="Sea Turtle", description="Navigation la plus paisible ayant valid? le parcours.", icon="??", is_exclusive=True),
            Badge(id="SNIPER", title="Sniper", description="Toutes les capsules valid?es ? 100% avec pr?cision (< 50 cm).", icon="??", is_exclusive=True),
            Badge(id="NAVIGATOR", title="Navigator", description="Contournement de la bou?e cardinale IALA conforme ? la r?gle maritime.", icon="??", is_exclusive=False),
            Badge(id="DRIFT_MASTER", title="Drift Master", description="Parcours valid? sans jamais sortir du couloir de d?rive tol?r?.", icon="??", is_exclusive=False),
            Badge(id="TITANIC", title="Titanic", description="Collision fracassante avec la jet?e.", icon="??", is_exclusive=False),
            Badge(id="NIGHT_OWL", title="Night Owl", description="?valuation d?clench?e entre 23h et 4h du matin.", icon="??", is_exclusive=False),
            Badge(id="EARLY_BIRD", title="Early Bird", description="Premi?re ?quipe ? ouvrir une PR franchissant au moins 3 portes.", icon="??", is_exclusive=False),
            Badge(id="MINIMALIST", title="Minimalist", description="Validation du parcours avec le minimum de soumissions.", icon="??", is_exclusive=True)
        ]
        for b in badges_data:
            existing_b = db.query(Badge).filter(Badge.id == b.id).first()
            if not existing_b:
                db.add(b)

        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Ocean Regatta - Scoreboard API",
    version="2.0.0",
    lifespan=lifespan
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
os.makedirs(static_dir, exist_ok=True)
os.makedirs(templates_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)

COMPETITION_SECRET_TOKEN = os.getenv("COMPETITION_SECRET_TOKEN", "ocean_regatta_super_secret_token_2026")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class RunSubmission(BaseModel):
    edition: str = "2026"
    student: str
    commit_sha: str
    tag: str
    score: int
    sim_time: float
    waypoints_cleared: int
    total_waypoints: int = 4
    success: bool
    collision: bool = False
    critical_drift_exceeded: bool = False
    reason: str = ""

def evaluate_and_update_badges(db: Session, edition_id: str, student: Student, new_run: Run):
    def award_badge(badge_id: str, exclusive: bool = False):
        if exclusive:
            db.query(StudentBadge).filter(
                StudentBadge.edition_id == edition_id,
                StudentBadge.badge_id == badge_id
            ).delete()
            db.flush()

        already = db.query(StudentBadge).filter(
            StudentBadge.edition_id == edition_id,
            StudentBadge.student_id == student.id,
            StudentBadge.badge_id == badge_id
        ).first()

        if not already:
            sb = StudentBadge(
                edition_id=edition_id,
                student_id=student.id,
                badge_id=badge_id,
                run_id=new_run.id,
                awarded_at=datetime.utcnow()
            )
            db.add(sb)
            db.flush()

    sub_hour = new_run.submitted_at.hour
    if sub_hour >= 23 or sub_hour < 4:
        award_badge("NIGHT_OWL", exclusive=False)

    if new_run.collision:
        award_badge("TITANIC", exclusive=False)

    if new_run.success and not new_run.critical_drift_exceeded:
        award_badge("DRIFT_MASTER", exclusive=False)

    if new_run.success:
        fastest = db.query(Run).filter(Run.edition_id == edition_id, Run.success == True).order_by(asc(Run.sim_time)).first()
        if fastest and fastest.student_id == student.id:
            award_badge("SPEED_DEMON", exclusive=True)

        slowest = db.query(Run).filter(Run.edition_id == edition_id, Run.success == True).order_by(desc(Run.sim_time)).first()
        if slowest and slowest.student_id == student.id:
            award_badge("SEA_TURTLE", exclusive=True)

    success_students = db.query(Student.id).join(Run).filter(Run.edition_id == edition_id, Run.success == True).distinct().all()
    if success_students:
        min_runs = 999999
        minimalist_id = None
        for s_tup in success_students:
            s_id = s_tup[0]
            cnt = db.query(func.count(Run.id)).filter(Run.edition_id == edition_id, Run.student_id == s_id).scalar()
            if cnt < min_runs:
                min_runs = cnt
                minimalist_id = s_id

        if minimalist_id:
            db.query(StudentBadge).filter(
                StudentBadge.edition_id == edition_id,
                StudentBadge.badge_id == "MINIMALIST"
            ).delete()
            db.flush()
            sb = StudentBadge(
                edition_id=edition_id,
                student_id=minimalist_id,
                badge_id="MINIMALIST",
                run_id=None,
                awarded_at=datetime.utcnow()
            )
            db.add(sb)
            db.flush()

@app.post("/api/submit_run")
def submit_run(
    payload: RunSubmission,
    db: Session = Depends(get_db),
    x_competition_token: Optional[str] = Header(None)
):
    if x_competition_token != COMPETITION_SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid competition token")

    edition = db.query(Edition).filter(Edition.id == payload.edition).first()
    if not edition:
        edition = Edition(id=payload.edition, year=int(payload.edition), name=f"Ocean Regatta {payload.edition}", is_active=True)
        db.add(edition)
        db.flush()

    student = db.query(Student).filter(Student.github_handle == payload.student).first()
    if not student:
        student = Student(github_handle=payload.student, display_name=payload.student)
        db.add(student)
        db.flush()

    run = Run(
        edition_id=edition.id,
        student_id=student.id,
        commit_sha=payload.commit_sha,
        tag=payload.tag,
        score=payload.score,
        sim_time=payload.sim_time,
        waypoints_cleared=payload.waypoints_cleared,
        total_waypoints=payload.total_waypoints,
        success=payload.success,
        collision=payload.collision,
        critical_drift_exceeded=payload.critical_drift_exceeded,
        reason=payload.reason,
        submitted_at=datetime.utcnow()
    )
    db.add(run)
    db.flush()

    evaluate_and_update_badges(db, edition.id, student, run)
    db.commit()

    return {"status": "success", "run_id": run.id, "edition": edition.id, "student": student.github_handle}

@app.get("/api/editions")
def list_editions(db: Session = Depends(get_db)):
    return db.query(Edition).order_by(desc(Edition.year)).all()

@app.get("/api/leaderboard")
def api_leaderboard(edition: str = "2026", db: Session = Depends(get_db)):
    students = db.query(Student).all()
    results = []
    for s in students:
        best_run = db.query(Run).filter(Run.edition_id == edition, Run.student_id == s.id).order_by(
            desc(Run.score), asc(Run.sim_time)
        ).first()
        if best_run:
            total_runs = db.query(func.count(Run.id)).filter(Run.edition_id == edition, Run.student_id == s.id).scalar()
            badges = [sb.badge.title for sb in s.badges if sb.edition_id == edition and sb.badge is not None]
            results.append({
                "github_handle": s.github_handle,
                "best_score": best_run.score,
                "best_time": best_run.sim_time,
                "success": best_run.success,
                "total_runs": total_runs,
                "badges": badges
            })
    results.sort(key=lambda x: (-x["best_score"], x["best_time"] if x["best_time"] > 0 else 999999))
    return results

@app.get("/", response_class=HTMLResponse)
def index_portal(request: Request, db: Session = Depends(get_db)):
    editions = db.query(Edition).order_by(desc(Edition.year)).all()
    active_edition = db.query(Edition).filter(Edition.is_active == True).first() or editions[0]

    students = db.query(Student).all()
    leaderboard = []
    for s in students:
        best = db.query(Run).filter(Run.edition_id == active_edition.id, Run.student_id == s.id).order_by(
            desc(Run.score), asc(Run.sim_time)
        ).first()
        if best:
            total_runs = db.query(func.count(Run.id)).filter(Run.edition_id == active_edition.id, Run.student_id == s.id).scalar()
            badges = [sb for sb in s.badges if sb.edition_id == active_edition.id and sb.badge is not None]
            leaderboard.append({
                "student": s,
                "best_run": best,
                "total_runs": total_runs,
                "badges": badges
            })

    leaderboard.sort(key=lambda x: (-x["best_run"].score, x["best_run"].sim_time if x["best_run"].sim_time > 0 else 999999))
    recent_runs = db.query(Run).order_by(desc(Run.submitted_at)).limit(8).all()
    all_badges = db.query(Badge).all()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "editions": editions,
            "active_edition": active_edition,
            "leaderboard": leaderboard,
            "recent_runs": recent_runs,
            "all_badges": all_badges
        }
    )

@app.get("/edition/{year}", response_class=HTMLResponse)
def edition_view(request: Request, year: str, db: Session = Depends(get_db)):
    edition = db.query(Edition).filter(Edition.id == year).first()
    if not edition:
        raise HTTPException(status_code=404, detail="?dition introuvable")

    students = db.query(Student).all()
    leaderboard = []
    for s in students:
        best = db.query(Run).filter(Run.edition_id == edition.id, Run.student_id == s.id).order_by(
            desc(Run.score), asc(Run.sim_time)
        ).first()
        if best:
            total = db.query(func.count(Run.id)).filter(Run.edition_id == edition.id, Run.student_id == s.id).scalar()
            badges = [sb for sb in s.badges if sb.edition_id == edition.id and sb.badge is not None]
            leaderboard.append({
                "student": s,
                "best_run": best,
                "total_runs": total,
                "badges": badges
            })

    leaderboard.sort(key=lambda x: (-x["best_run"].score, x["best_run"].sim_time if x["best_run"].sim_time > 0 else 999999))
    editions = db.query(Edition).order_by(desc(Edition.year)).all()

    return templates.TemplateResponse(
        request=request,
        name="edition.html",
        context={
            "request": request,
            "edition": edition,
            "editions": editions,
            "leaderboard": leaderboard
        }
    )

@app.get("/student/{github_handle}", response_class=HTMLResponse)
def student_view(request: Request, github_handle: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.github_handle == github_handle).first()
    if not student:
        raise HTTPException(status_code=404, detail="?tudiant introuvable")

    student_badges = [sb for sb in student.badges if sb.badge is not None]

    return templates.TemplateResponse(
        request=request,
        name="student.html",
        context={
            "request": request,
            "student": student,
            "runs": student.runs,
            "badges": student_badges
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
