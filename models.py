from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('sqlite:///fitness.db')
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    
    # Relationships
    workouts = relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, name, email):
        self.set_name(name)
        self.set_email(email)
    
    def set_name(self, name):
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters")
        self.name = name
    
    def set_email(self, email):
        if not email or '@' not in email:
            raise ValueError("Invalid email format")
        self.email = email
    
    @classmethod
    def create(cls, session, name, email):
        user = cls(name=name, email=email)
        session.add(user)
        session.commit()
        return user
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        user = cls.find_by_id(session, id)
        if user:
            session.delete(user)
            session.commit()
            return True
        return False


class Exercise(Base):
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    
    # Relationships
    workout_exercises = relationship("WorkoutExercise", back_populates="exercise", cascade="all, delete-orphan")
    
    def __init__(self, name, description=None):
        self.set_name(name)
        self.description = description
    
    def set_name(self, name):
        if not name or len(name) < 2:
            raise ValueError("Exercise name must be at least 2 characters")
        self.name = name
    
    @classmethod
    def create(cls, session, name, description=None):
        exercise = cls(name=name, description=description)
        session.add(exercise)
        session.commit()
        return exercise
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        exercise = cls.find_by_id(session, id)
        if exercise:
            session.delete(exercise)
            session.commit()
            return True
        return False


class Workout(Base):
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Relationships
    user = relationship("User", back_populates="workouts")
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")
    
    def __init__(self, name, user_id):
        self.set_name(name)
        self.user_id = user_id
    
    def set_name(self, name):
        if not name or len(name) < 2:
            raise ValueError("Workout name must be at least 2 characters")
        self.name = name
    
    @classmethod
    def create(cls, session, name, user_id):
        workout = cls(name=name, user_id=user_id)
        session.add(workout)
        session.commit()
        return workout
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        workout = cls.find_by_id(session, id)
        if workout:
            session.delete(workout)
            session.commit()
            return True
        return False


class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'
    
    id = Column(Integer, primary_key=True)
    workout_id = Column(Integer, ForeignKey('workouts.id'))
    exercise_id = Column(Integer, ForeignKey('exercises.id'))
    sets = Column(Integer, default=3)
    reps = Column(Integer, default=10)
    weight = Column(Float, default=0.0)
    
    # Relationships
    workout = relationship("Workout", back_populates="workout_exercises")
    exercise = relationship("Exercise", back_populates="workout_exercises")
    
    def __init__(self, workout_id, exercise_id, sets=3, reps=10, weight=0.0):
        self.workout_id = workout_id
        self.exercise_id = exercise_id
        self.set_sets(sets)
        self.set_reps(reps)
        self.set_weight(weight)
    
    def set_sets(self, sets):
        if sets < 0:
            raise ValueError("Sets cannot be negative")
        self.sets = sets
    
    def set_reps(self, reps):
        if reps < 0:
            raise ValueError("Reps cannot be negative")
        self.reps = reps
    
    def set_weight(self, weight):
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        self.weight = weight
    
    @classmethod
    def create(cls, session, workout_id, exercise_id, sets=3, reps=10, weight=0.0):
        workout_exercise = cls(workout_id=workout_id, exercise_id=exercise_id, 
                               sets=sets, reps=reps, weight=weight)
        session.add(workout_exercise)
        session.commit()
        return workout_exercise
    
    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()
    
    @classmethod
    def find_by_id(cls, session, id):
        return session.query(cls).filter_by(id=id).first()
    
    @classmethod
    def delete(cls, session, id):
        workout_exercise = cls.find_by_id(session, id)
        if workout_exercise:
            session.delete(workout_exercise)
            session.commit()
            return True
        return False

# Create database tables
Base.metadata.create_all(engine)