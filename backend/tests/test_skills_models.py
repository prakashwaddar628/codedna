import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

from app.models.base import Base
from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkill

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_skill(db_session: Session):
    # Verify we can create a skill
    skill = Skill(
        name="Python",
        category="Programming",
        description="Python programming language"
    )
    db_session.add(skill)
    db_session.commit()

    assert skill.id is not None
    assert skill.name == "Python"
    assert skill.category == "Programming"

def test_user_skill_relationship(db_session: Session):
    # Create user
    user = User(
        full_name="Prakash",
        email="prakash@example.com",
        hashed_password="fakehash"
    )
    db_session.add(user)
    db_session.commit()

    # Create skill
    skill = Skill(
        name="FastAPI",
        category="Backend",
        description="FastAPI framework"
    )
    db_session.add(skill)
    db_session.commit()

    # Link user and skill via UserSkill
    user_skill = UserSkill(
        user_id=user.id,
        skill_id=skill.id,
        level=8,
        confidence=7
    )
    db_session.add(user_skill)
    db_session.commit()

    # Verify relationships are loaded correctly
    assert len(user.user_skills) == 1
    assert user.user_skills[0].skill.name == "FastAPI"
    assert user.user_skills[0].level == 8
    assert user.user_skills[0].confidence == 7

    assert len(skill.user_skills) == 1
    assert skill.user_skills[0].user.full_name == "Prakash"

def test_user_skill_level_constraints(db_session: Session):
    user = User(full_name="Prakash", email="prakash@example.com", hashed_password="fakehash")
    skill = Skill(name="Docker", category="DevOps", description="Containerization")
    db_session.add_all([user, skill])
    db_session.commit()

    # Invalid level > 10
    invalid_skill_high = UserSkill(
        user_id=user.id,
        skill_id=skill.id,
        level=11,
        confidence=5
    )
    db_session.add(invalid_skill_high)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    # Invalid level < 1
    invalid_skill_low = UserSkill(
        user_id=user.id,
        skill_id=skill.id,
        level=0,
        confidence=5
    )
    db_session.add(invalid_skill_low)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_skill_confidence_constraints(db_session: Session):
    user = User(full_name="Prakash", email="prakash@example.com", hashed_password="fakehash")
    skill = Skill(name="Docker", category="DevOps", description="Containerization")
    db_session.add_all([user, skill])
    db_session.commit()

    # Invalid confidence > 10
    invalid_skill_high = UserSkill(
        user_id=user.id,
        skill_id=skill.id,
        level=5,
        confidence=12
    )
    db_session.add(invalid_skill_high)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_skill_unique_constraint(db_session: Session):
    user = User(full_name="Prakash", email="prakash@example.com", hashed_password="fakehash")
    skill = Skill(name="Docker", category="DevOps", description="Containerization")
    db_session.add_all([user, skill])
    db_session.commit()

    # Create first entry
    us1 = UserSkill(user_id=user.id, skill_id=skill.id, level=5, confidence=5)
    db_session.add(us1)
    db_session.commit()

    # Attempt to create duplicate entry
    us2 = UserSkill(user_id=user.id, skill_id=skill.id, level=7, confidence=7)
    db_session.add(us2)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

def test_user_skill_cascade_delete(db_session: Session):
    user = User(full_name="Prakash", email="prakash@example.com", hashed_password="fakehash")
    skill = Skill(name="Docker", category="DevOps", description="Containerization")
    db_session.add_all([user, skill])
    db_session.commit()

    us = UserSkill(user_id=user.id, skill_id=skill.id, level=5, confidence=5)
    db_session.add(us)
    db_session.commit()

    # Delete User and verify cascade
    db_session.delete(user)
    db_session.commit()

    # Verify UserSkill record is also deleted
    remaining = db_session.query(UserSkill).filter_by(user_id=user.id).all()
    assert len(remaining) == 0
