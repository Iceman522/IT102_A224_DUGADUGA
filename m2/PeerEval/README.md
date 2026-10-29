
# PeerEval

## Project Description
PeerEval is a Python OOP-based decision support system that helps students submit structured peer evaluations and enables instructors to track team performance and variance analytics.

## High-Priority Features
1. Role-Based Access Control (RBAC) for students and instructors
2. Rubric-based peer evaluation submission (Communication, Effort, Technical Quality)
3. DSS variance analytics ($\sigma$) for tracking team friction and free-riding
4. Automated PDF and CSV report generation using ReportLab and Pandas
5. Instructor dashboard for monitoring group health and managing cohorts

## Technologies Used
- Python
- Streamlit
- SQLite (`sqlite3`)
- ReportLab
- Pandas

## OOP Implementation
- Encapsulation: Core data structures and domain logic are bundled into dedicated classes (`User`, `ProjectGroup`, `PeerEvaluation`).
- Inheritance: Specialized subclasses (`Student` and `Instructor`) extend the base `User` class to manage role-specific permissions.
- Polymorphism: Analytical methods and views handle role-specific behaviors dynamically.
- Abstraction: Controllers and service layers isolate business rules from UI rendering.

## Project Structure
- `app.py`: Main application entry point
- `models.py`: Core domain classes and database schema operations
- `controllers.py`: Business logic and session/state management
- `views.py`: Streamlit user interface components and layout
- `peereval.db`: Embedded SQLite database for local persistence

## Installation
1. Download or clone the repository.
2. Create and activate a Python virtual environment.
3. Install the required packages: pip install streamlit reportlab pandas
4. Run the application using Streamlit: streamlit run app.py

## Developers
- Adrian Paolo V. Dugaduga
4. Install the required packages:
   ```bash
   pip install streamlit reportlab pandas
