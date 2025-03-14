from models import Session, User, Exercise, Workout, WorkoutExercise
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_data(session):
    """Clear existing data from all tables"""
    try:
        logger.info("Clearing existing data...")
        session.query(WorkoutExercise).delete()
        session.query(Workout).delete()
        session.query(Exercise).delete()
        session.query(User).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error clearing data: {e}")
        raise

def seed_users(session):
    """Seed users table with sample data"""
    users = [
        User(name="John Doe", email="john.doe@example.com"),
        User(name="Jane Smith", email="jane.smith@example.com"),
        User(name="Mike Johnson", email="mike.johnson@example.com"),
        User(name="Sarah Wilson", email="sarah.wilson@example.com")
    ]
    session.add_all(users)
    session.commit()
    logger.info(f"Added {len(users)} users")
    return users

def seed_exercises(session):
    """Seed exercises table with common exercises"""
    exercises = [
        Exercise(
            name="Push-ups",
            description="A bodyweight exercise that targets chest, shoulders, and triceps. Start in a plank position and lower your body until your chest nearly touches the ground, then push back up."
        ),
        Exercise(
            name="Pull-ups",
            description="An upper body compound exercise performed on a bar. Hang with arms extended, then pull yourself up until your chin is over the bar."
        ),
        Exercise(
            name="Squats",
            description="A fundamental lower body exercise. Stand with feet shoulder-width apart, lower your body by bending knees and hips, then return to standing."
        ),
        Exercise(
            name="Plank",
            description="A core strengthening exercise. Hold a push-up position with your body forming a straight line from head to heels."
        ),
        Exercise(
            name="Deadlift",
            description="A compound exercise that works multiple muscle groups. Lift a weighted barbell from the ground to hip level while maintaining a straight back."
        ),
        Exercise(
            name="Bench Press",
            description="A upper body strength exercise. Lie on a bench and push a weighted barbell up from chest level to full arm extension."
        ),
        Exercise(
            name="Lunges",
            description="A lower body exercise that works legs and improves balance. Step forward with one leg and lower your body until both knees are bent at 90 degrees."
        ),
        Exercise(
            name="Shoulder Press",
            description="An upper body exercise targeting shoulders. Press weights from shoulder level straight up overhead until arms are fully extended."
        )
    ]
    session.add_all(exercises)
    session.commit()
    logger.info(f"Added {len(exercises)} exercises")
    return exercises

def seed_workouts(session, users):
    """Seed workouts table with sample data"""
    workouts = [
        Workout(
            user_id=users[0].id,
            name="Morning Strength Training"
        ),
        Workout(
            user_id=users[0].id,
            name="Evening Cardio"
        ),
        Workout(
            user_id=users[1].id,
            name="Full Body Workout"
        ),
        Workout(
            user_id=users[2].id,
            name="Upper Body Focus"
        ),
        Workout(
            user_id=users[3].id,
            name="Lower Body Day"
        )
    ]
    session.add_all(workouts)
    session.commit()
    logger.info(f"Added {len(workouts)} workouts")
    return workouts

def seed_workout_exercises(session, workouts, exercises):
    """Seed workout_exercises table linking workouts and exercises"""
    workout_exercises = [
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[0].id, sets=3, reps=15),
        WorkoutExercise(workout_id=workouts[0].id, exercise_id=exercises[1].id, sets=3, reps=10),
        WorkoutExercise(workout_id=workouts[1].id, exercise_id=exercises[2].id, sets=4, reps=12),
        WorkoutExercise(workout_id=workouts[2].id, exercise_id=exercises[3].id, sets=3, reps=60),
        WorkoutExercise(workout_id=workouts[3].id, exercise_id=exercises[4].id, sets=5, reps=5),
        WorkoutExercise(workout_id=workouts[4].id, exercise_id=exercises[5].id, sets=4, reps=8)
    ]
    session.add_all(workout_exercises)
    session.commit()
    logger.info(f"Added {len(workout_exercises)} workout exercises")

def main():
    """Main function to seed the database"""
    session = Session()
    try:
        logger.info("Starting database seeding...")
        clear_data(session)
        users = seed_users(session)
        exercises = seed_exercises(session)
        workouts = seed_workouts(session, users)
        seed_workout_exercises(session, workouts, exercises)
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()