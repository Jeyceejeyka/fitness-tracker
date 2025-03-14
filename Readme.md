# Fitness Tracker Application

A command-line application for tracking workouts and exercises, built with Python and SQLAlchemy.

## Project Description

This Fitness Tracker allows users to:
- Manage user profiles
- Track workouts
- Record exercises
- Monitor workout progress
- Store workout history

## Tech Stack

- Python 3.8+
- SQLAlchemy (ORM)
- SQLite (Database)
- Alembic (Database migrations)

## Project Structure

```
fitness-tracker/
├── myCodes/
│   ├── __init__.py
│   ├── app.py         # Application entry point
│   ├── cli.py         # Command-line interface
│   ├── models.py      # Database models
│   └── seed.py        # Database seeding script
├── migrations/
│   ├── env.py
│   └── ...           # Migration files
├── alembic.ini        # Alembic configuration
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fitness-tracker
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
cd myCodes
python3 -c "from models import Base, engine; Base.metadata.create_all(engine)"
```

5. Seed the database with sample data:
```bash
python3 seed.py
```

## Database Models

- **User**: Stores user information
- **Exercise**: Contains exercise definitions and descriptions
- **Workout**: Records workout sessions
- **WorkoutExercise**: Links exercises to workouts with sets and reps

## Usage

Run the application:
```bash
cd myCodes
python3 app.py
```

## Features

- User management
- Exercise library
- Workout tracking
- Progress monitoring
- Detailed exercise descriptions
- Multiple workout types support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- SQLAlchemy documentation
- Python command-line interface best practices
- Fitness tracking methodologies