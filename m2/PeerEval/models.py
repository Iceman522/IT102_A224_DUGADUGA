import math
import sqlite3
from typing import List, Dict, Optional

# ==========================================
# 1. CORE DOMAIN CLASSES (OOP)
# ==========================================
class User:
    def __init__(self, user_id: str, name: str, role: str):
        self.user_id = user_id
        self.name = name
        self.role = role

class Student(User):
    def __init__(self, user_id: str, name: str, role: str, group_id: str):
        super().__init__(user_id, name, role)
        self.group_id = group_id

class Instructor(User):
    def __init__(self, user_id: str, name: str, role: str, department: str):
        super().__init__(user_id, name, role)
        self.department = department

class ProjectGroup:
    def __init__(self, group_id: str, group_name: str, members: List[Student]):
        self.group_id = group_id
        self.group_name = group_name
        self.members = members

class PeerEvaluation:
    def __init__(self, eval_id: str, evaluator_id: str, evaluatee_id: str, 
                 communication_score: int, effort_score: int, technical_score: int, feedback: str):
        self.eval_id = eval_id
        self.evaluator_id = evaluator_id
        self.evaluatee_id = evaluatee_id
        self.communication_score = communication_score
        self.effort_score = effort_score
        self.technical_score = technical_score
        self.feedback = feedback
        
        # Calculate weighted average score automatically
        self.average_score = round((communication_score + effort_score + technical_score) / 3.0, 2)


# ==========================================
# 2. DECISION SUPPORT SYSTEM (DSS) ANALYZER
# ==========================================
class GroupHealthAnalyzer:
    def __init__(self, variance_threshold: float = 1.2, low_score_threshold: float = 2.5):
        self.variance_threshold = variance_threshold
        self.low_score_threshold = low_score_threshold

    def analyze_health(self, group_members: List, evaluations: List) -> Dict:
        if not evaluations:
            return {
                "status": "No Data",
                "badge_color": "gray",
                "avg_score": 0.0,
                "variance": 0.0,
                "sigma": 0.0,
                "flag": False,
                "msg": "No evaluations submitted yet for this team.",
                "recommendation": "Encourage group members to complete peer reviews before the deadline.",
                "freeloaders": []
            }

        scores = [e.average_score for e in evaluations]
        avg_score = sum(scores) / len(scores)

        # Statistical Sample Variance (sigma squared) and Standard Deviation (sigma)
        if len(scores) > 1:
            variance = sum((x - avg_score) ** 2 for x in scores) / (len(scores) - 1)
            sigma = math.sqrt(variance)
        else:
            variance = 0.0
            sigma = 0.0

        student_received_scores: Dict[str, List[float]] = {m.user_id: [] for m in group_members}
        for e in evaluations:
            if e.evaluatee_id in student_received_scores:
                student_received_scores[e.evaluatee_id].append(e.average_score)

        freeloaders = []
        for student_id, received in student_received_scores.items():
            if received:
                student_avg = sum(received) / len(received)
                if student_avg < self.low_score_threshold:
                    freeloaders.append(student_id)

        has_flag = (sigma > self.variance_threshold) or (len(freeloaders) > 0) or (avg_score < self.low_score_threshold)

        if len(freeloaders) > 0:
            status = "Critical Conflict"
            badge_color = "red"
            msg = f"Potential freeloading detected ({len(freeloaders)} member(s) scored below acceptable rubric baseline)."
            recommendation = "Schedule an immediate team check-in to reassign task modules and rebalance deliverables."
        elif sigma > self.variance_threshold:
            status = "Warning"
            badge_color = "orange"
            msg = f"Statistically significant score variance observed (σ = {round(sigma, 2)})."
            recommendation = "Review individual qualitative feedback to resolve communication bottlenecks or mismatched expectations."
        else:
            status = "Healthy"
            badge_color = "green"
            msg = "Group evaluation scores indicate balanced team contribution and high mutual trust."
            recommendation = "Team collaboration is optimal. Proceed with standard sprint monitoring."

        return {
            "status": status,
            "badge_color": badge_color,
            "avg_score": round(avg_score, 2),
            "variance": round(variance, 2),
            "sigma": round(sigma, 2),
            "flag": has_flag,
            "msg": msg,
            "recommendation": recommendation,
            "freeloaders": freeloaders
        }


# ==========================================
# 3. RELATIONAL SQLITE STORAGE UTILITY
# ==========================================
class DataStorage:
    DB_NAME = "peereval.db"

    @classmethod
    def initialize_db(cls):
        """Creates the necessary SQLite relational table if it doesn't exist."""
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS evaluations (
                eval_id TEXT PRIMARY KEY,
                evaluator_id TEXT,
                evaluatee_id TEXT,
                communication_score INTEGER,
                effort_score INTEGER,
                technical_score INTEGER,
                average_score REAL,
                feedback TEXT
            )
        ''')
        
        conn.commit()
        conn.close()

    @classmethod
    def save_evaluation(cls, eval_obj: PeerEvaluation):
        """Saves or updates a single peer evaluation record inside SQLite."""
        cls.initialize_db()
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO evaluations 
            (eval_id, evaluator_id, evaluatee_id, communication_score, effort_score, technical_score, average_score, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            eval_obj.eval_id,
            eval_obj.evaluator_id,
            eval_obj.evaluatee_id,
            eval_obj.communication_score,
            eval_obj.effort_score,
            eval_obj.technical_score,
            eval_obj.average_score,
            eval_obj.feedback
        ))
        
        conn.commit()
        conn.close()

    @classmethod
    def save_evaluations(cls, evaluations: List[PeerEvaluation]):
        """Bulk saves a list of evaluation objects."""
        for e in evaluations:
            cls.save_evaluation(e)

    @classmethod
    def load_evaluations(cls) -> List[PeerEvaluation]:
        """Queries and loads all peer evaluations from the relational SQLite database."""
        cls.initialize_db()
        conn = sqlite3.connect(cls.DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("SELECT eval_id, evaluator_id, evaluatee_id, communication_score, effort_score, technical_score, feedback FROM evaluations")
        rows = cursor.fetchall()
        conn.close()
        
        evaluations = []
        for row in rows:
            eval_id, evaluator_id, evaluatee_id, comm, effort, tech, feedback = row
            evaluations.append(
                PeerEvaluation(
                    eval_id=eval_id,
                    evaluator_id=evaluator_id,
                    evaluatee_id=evaluatee_id,
                    communication_score=comm,
                    effort_score=effort,
                    technical_score=tech,
                    feedback=feedback
                )
            )
        return evaluations