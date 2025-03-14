from models import Session, User, Exercise, Workout, WorkoutExercise
import sys

def clear_screen():
    print("\n" * 5)

def print_menu(title, options):
    clear_screen()
    print(f"===== {title} =====")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("0. Back")
    
    choice = input("\nEnter your choice: ")
    return choice

def safe_input(prompt, validator=None, error_msg=None):
    while True:
        value = input(prompt)
        if validator is None or validator(value):
            return value
        print(error_msg or "Invalid input, please try again.")

def main_menu():
    options = [
        "User Management",
        "Exercise Management",
        "Workout Management",
        "Workout Exercise Management",
        "Exit"
    ]
    
    while True:
        choice = print_menu("FITNESS TRACKER MAIN MENU", options)
        
        if choice == "1":
            user_menu()
        elif choice == "2":
            exercise_menu()
        elif choice == "3":
            workout_menu()
        elif choice == "4":
            workout_exercise_menu()
        elif choice == "5" or choice == "0":
            print("Goodbye!")
            sys.exit(0)
        else:
            input("Invalid choice. Press Enter to continue...")

def user_menu():
    session = Session()
    
    options = [
        "Create New User",
        "View All Users",
        "Find User by ID",
        "Delete User",
        "View User's Workouts"
    ]
    
    while True:
        choice = print_menu("USER MANAGEMENT", options)
        
        if choice == "1":
            try:
                name = safe_input("Enter name: ", lambda x: len(x) >= 2, "Name must be at least 2 characters")
                email = safe_input("Enter email: ", lambda x: '@' in x, "Email must contain @")
                user = User.create(session, name, email)
                print(f"User created with ID {user.id}")
            except ValueError as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
            
        elif choice == "2":
            users = User.get_all(session)
            if users:
                print("\nAll Users:")
                for user in users:
                    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
            else:
                print("No users found.")
            input("Press Enter to continue...")
            
        elif choice == "3":
            try:
                id = int(safe_input("Enter user ID: ", lambda x: x.isdigit(), "ID must be a number"))
                user = User.find_by_id(session, id)
                if user:
                    print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "4":
            try:
                id = int(safe_input("Enter user ID to delete: ", lambda x: x.isdigit(), "ID must be a number"))
                if User.delete(session, id):
                    print("User deleted successfully.")
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "5":
            try:
                id = int(safe_input("Enter user ID: ", lambda x: x.isdigit(), "ID must be a number"))
                user = User.find_by_id(session, id)
                if user:
                    if user.workouts:
                        print(f"\nWorkouts for {user.name}:")
                        for workout in user.workouts:
                            print(f"ID: {workout.id}, Name: {workout.name}, Date: {workout.date}")
                    else:
                        print(f"{user.name} has no workouts.")
                else:
                    print("User not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "0":
            session.close()
            return
        else:
            input("Invalid choice. Press Enter to continue...")

def exercise_menu():
    session = Session()
    
    options = [
        "Create New Exercise",
        "View All Exercises",
        "Find Exercise by ID",
        "Delete Exercise",
        "View Exercise Usage in Workouts"
    ]
    
    while True:
        choice = print_menu("EXERCISE MANAGEMENT", options)
        
        if choice == "1":
            try:
                name = safe_input("Enter exercise name: ", lambda x: len(x) >= 2, "Name must be at least 2 characters")
                description = input("Enter description (optional): ")
                exercise = Exercise.create(session, name, description)
                print(f"Exercise created with ID {exercise.id}")
            except ValueError as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
            
        elif choice == "2":
            exercises = Exercise.get_all(session)
            if exercises:
                print("\nAll Exercises:")
                for exercise in exercises:
                    print(f"ID: {exercise.id}, Name: {exercise.name}, Description: {exercise.description}")
            else:
                print("No exercises found.")
            input("Press Enter to continue...")
            
        elif choice == "3":
            try:
                id = int(safe_input("Enter exercise ID: ", lambda x: x.isdigit(), "ID must be a number"))
                exercise = Exercise.find_by_id(session, id)
                if exercise:
                    print(f"ID: {exercise.id}, Name: {exercise.name}, Description: {exercise.description}")
                else:
                    print("Exercise not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "4":
            try:
                id = int(safe_input("Enter exercise ID to delete: ", lambda x: x.isdigit(), "ID must be a number"))
                if Exercise.delete(session, id):
                    print("Exercise deleted successfully.")
                else:
                    print("Exercise not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "5":
            try:
                id = int(safe_input("Enter exercise ID: ", lambda x: x.isdigit(), "ID must be a number"))
                exercise = Exercise.find_by_id(session, id)
                if exercise:
                    if exercise.workout_exercises:
                        print(f"\nWorkouts containing {exercise.name}:")
                        for we in exercise.workout_exercises:
                            print(f"Workout ID: {we.workout.id}, Name: {we.workout.name}, Sets: {we.sets}, Reps: {we.reps}, Weight: {we.weight}")
                    else:
                        print(f"{exercise.name} is not used in any workouts.")
                else:
                    print("Exercise not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "0":
            session.close()
            return
        else:
            input("Invalid choice. Press Enter to continue...")

def workout_menu():
    session = Session()
    
    options = [
        "Create New Workout",
        "View All Workouts",
        "Find Workout by ID",
        "Delete Workout",
        "View Workout Exercises"
    ]
    
    while True:
        choice = print_menu("WORKOUT MANAGEMENT", options)
        
        if choice == "1":
            try:
                name = safe_input("Enter workout name: ", lambda x: len(x) >= 2, "Name must be at least 2 characters")
                
                # Show users to choose from
                users = User.get_all(session)
                if not users:
                    print("No users found. Please create a user first.")
                    input("Press Enter to continue...")
                    continue
                
                print("\nAvailable Users:")
                for user in users:
                    print(f"ID: {user.id}, Name: {user.name}")
                
                user_id = int(safe_input("Enter user ID: ", lambda x: x.isdigit(), "ID must be a number"))
                if not User.find_by_id(session, user_id):user = User.find_by_id(session, user_id)
                if not user:
                    print("User not found.")
                    input("Press Enter to continue...")
                    continue
                
                workout = Workout.create(session, name, user_id)
                print(f"Workout created with ID {workout.id}")
            except ValueError as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
            
        elif choice == "2":
            workouts = Workout.get_all(session)
            if workouts:
                print("\nAll Workouts:")
                for workout in workouts:
                    print(f"ID: {workout.id}, Name: {workout.name}, Date: {workout.date}, User: {workout.user.name}")
            else:
                print("No workouts found.")
            input("Press Enter to continue...")
            
        elif choice == "3":
            try:
                id = int(safe_input("Enter workout ID: ", lambda x: x.isdigit(), "ID must be a number"))
                workout = Workout.find_by_id(session, id)
                if workout:
                    print(f"ID: {workout.id}, Name: {workout.name}, Date: {workout.date}, User: {workout.user.name}")
                else:
                    print("Workout not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "4":
            try:
                id = int(safe_input("Enter workout ID to delete: ", lambda x: x.isdigit(), "ID must be a number"))
                if Workout.delete(session, id):
                    print("Workout deleted successfully.")
                else:
                    print("Workout not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "5":
            try:
                id = int(safe_input("Enter workout ID: ", lambda x: x.isdigit(), "ID must be a number"))
                workout = Workout.find_by_id(session, id)
                if workout:
                    if workout.workout_exercises:
                        print(f"\nExercises in '{workout.name}':")
                        for we in workout.workout_exercises:
                            print(f"Exercise: {we.exercise.name}, Sets: {we.sets}, Reps: {we.reps}, Weight: {we.weight}")
                    else:
                        print(f"Workout '{workout.name}' doesn't have any exercises.")
                else:
                    print("Workout not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "0":
            session.close()
            return
        else:
            input("Invalid choice. Press Enter to continue...")

def workout_exercise_menu():
    session = Session()
    
    options = [
        "Add Exercise to Workout",
        "View All Workout Exercises",
        "Find Workout Exercise by ID",
        "Update Sets/Reps/Weight",
        "Remove Exercise from Workout"
    ]
    
    while True:
        choice = print_menu("WORKOUT EXERCISE MANAGEMENT", options)
        
        if choice == "1":
            try:
                # Show workouts to choose from
                workouts = Workout.get_all(session)
                if not workouts:
                    print("No workouts found. Please create a workout first.")
                    input("Press Enter to continue...")
                    continue
                
                print("\nAvailable Workouts:")
                for workout in workouts:
                    print(f"ID: {workout.id}, Name: {workout.name}, User: {workout.user.name}")
                
                workout_id = int(safe_input("Enter workout ID: ", lambda x: x.isdigit(), "ID must be a number"))
                if not Workout.find_by_id(session, workout_id):
                    print("Workout not found.")
                    input("Press Enter to continue...")
                    continue
                
                # Show exercises to choose from
                exercises = Exercise.get_all(session)
                if not exercises:
                    print("No exercises found. Please create an exercise first.")
                    input("Press Enter to continue...")
                    continue
                
                print("\nAvailable Exercises:")
                for exercise in exercises:
                    print(f"ID: {exercise.id}, Name: {exercise.name}")
                
                exercise_id = int(safe_input("Enter exercise ID: ", lambda x: x.isdigit(), "ID must be a number"))
                if not Exercise.find_by_id(session, exercise_id):
                    print("Exercise not found.")
                    input("Press Enter to continue...")
                    continue
                
                sets = int(safe_input("Enter number of sets: ", lambda x: x.isdigit(), "Sets must be a number"))
                reps = int(safe_input("Enter number of reps: ", lambda x: x.isdigit(), "Reps must be a number"))
                weight = float(safe_input("Enter weight (kg): ", lambda x: x.replace('.', '', 1).isdigit(), "Weight must be a number"))
                
                workout_exercise = WorkoutExercise.create(session, workout_id, exercise_id, sets, reps, weight)
                print(f"Exercise added to workout with ID {workout_exercise.id}")
            except ValueError as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
            
        elif choice == "2":
            workout_exercises = WorkoutExercise.get_all(session)
            if workout_exercises:
                print("\nAll Workout Exercises:")
                for we in workout_exercises:
                    print(f"ID: {we.id}, Workout: {we.workout.name}, Exercise: {we.exercise.name}, " 
                          f"Sets: {we.sets}, Reps: {we.reps}, Weight: {we.weight}")
            else:
                print("No workout exercises found.")
            input("Press Enter to continue...")
            
        elif choice == "3":
            try:
                id = int(safe_input("Enter workout exercise ID: ", lambda x: x.isdigit(), "ID must be a number"))
                we = WorkoutExercise.find_by_id(session, id)
                if we:
                    print(f"ID: {we.id}, Workout: {we.workout.name}, Exercise: {we.exercise.name}, "
                          f"Sets: {we.sets}, Reps: {we.reps}, Weight: {we.weight}")
                else:
                    print("Workout exercise not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "4":
            try:
                id = int(safe_input("Enter workout exercise ID: ", lambda x: x.isdigit(), "ID must be a number"))
                we = WorkoutExercise.find_by_id(session, id)
                if we:
                    print(f"Current: Sets: {we.sets}, Reps: {we.reps}, Weight: {we.weight}")
                    sets = int(safe_input("Enter new number of sets: ", lambda x: x.isdigit(), "Sets must be a number"))
                    reps = int(safe_input("Enter new number of reps: ", lambda x: x.isdigit(), "Reps must be a number"))
                    weight = float(safe_input("Enter new weight (kg): ", lambda x: x.replace('.', '', 1).isdigit(), "Weight must be a number"))
                    
                    we.set_sets(sets)
                    we.set_reps(reps)
                    we.set_weight(weight)
                    session.commit()
                    print("Workout exercise updated successfully.")
                else:
                    print("Workout exercise not found.")
            except ValueError as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
            
        elif choice == "5":
            try:
                id = int(safe_input("Enter workout exercise ID to remove: ", lambda x: x.isdigit(), "ID must be a number"))
                if WorkoutExercise.delete(session, id):
                    print("Exercise removed from workout successfully.")
                else:
                    print("Workout exercise not found.")
            except ValueError:
                print("Invalid ID format.")
            input("Press Enter to continue...")
            
        elif choice == "0":
            session.close()
            return
        else:
            input("Invalid choice. Press Enter to continue...")

if __name__ == "__main__":
    main_menu()