from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Edition(Base):
    __tablename__ = "editions"

    id = Column(String(20), primary_key=True)
    year = Column(Integer, nullable=False, unique=True)
    name = Column(String(120), nullable=False)
    is_active = Column(Boolean, default=False)
    description = Column(Text, default="")
    template_url = Column(String(255), default="")

    runs = relationship("Run", back_populates="edition", cascade="all, delete-orphan")
    student_badges = relationship("StudentBadge", back_populates="edition", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    github_handle = Column(String(100), unique=True, index=True, nullable=False)
    display_name = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    runs = relationship("Run", back_populates="student", cascade="all, delete-orphan", order_by="desc(Run.submitted_at)")
    badges = relationship("StudentBadge", back_populates="student", cascade="all, delete-orphan")


class Run(Base):
    __tablename__ = "runs"

    id = Column(Integer, primary_key=True, index=True)
    edition_id = Column(String(20), ForeignKey("editions.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    commit_sha = Column(String(64), nullable=False)
    tag = Column(String(120), nullable=False)
    score = Column(Integer, default=0, nullable=False)
    sim_time = Column(Float, default=0.0, nullable=False)
    waypoints_cleared = Column(Integer, default=0, nullable=False)
    total_waypoints = Column(Integer, default=4, nullable=False)
    success = Column(Boolean, default=False, nullable=False)
    collision = Column(Boolean, default=False, nullable=False)
    critical_drift_exceeded = Column(Boolean, default=False, nullable=False)
    reason = Column(Text, default="", nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, index=True)

    edition = relationship("Edition", back_populates="runs")
    student = relationship("Student", back_populates="runs")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(String(50), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(20), default="🎖️")
    is_exclusive = Column(Boolean, default=False)

    student_badges = relationship("StudentBadge", back_populates="badge")


class StudentBadge(Base):
    __tablename__ = "student_badges"

    id = Column(Integer, primary_key=True, index=True)
    edition_id = Column(String(20), ForeignKey("editions.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    badge_id = Column(String(50), ForeignKey("badges.id"), nullable=False)
    awarded_at = Column(DateTime, default=datetime.utcnow)
    run_id = Column(Integer, ForeignKey("runs.id"), nullable=True)

    edition = relationship("Edition", back_populates="student_badges")
    student = relationship("Student", back_populates="badges")
    badge = relationship("Badge", back_populates="student_badges")
