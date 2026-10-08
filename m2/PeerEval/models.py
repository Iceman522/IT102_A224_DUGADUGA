import json
import os
import math
from dataclasses import dataclass, field, asdict
from typing import List, Dict

@dataclass
class User:
    user_id: str
    name: str
    role: str  # "Student" or "Instructor"

@dataclass
class Student(User):
    group_id: str = ""

@dataclass
class Instructor(User):
    department: str = "Information Systems"

@dataclass
class ProjectGroup:
    group_id: str
    group_name: str
    members: List[Student] = field(default_factory=list)

@dataclass
class PeerEvaluation:
    eval_id: str
    evaluator_id: str
    evaluatee_id: str
    communication_score: int
    effort_score: int
    technical_score: int
    feedback: str

    @property
    def average_score(self) -> float:
        return (self.communication_score + self.effort_score + self.technical_score) / 3.0

class GroupHealthAnalyzer:
    def __init__(self, variance_threshold: float = 1.0, low_score_threshold: float = 2.5):
        self.variance_threshold = variance_threshold
        self.low_score_threshold = low_score_threshold

    def analyze_health(self, group_members: List[Student], evaluations: List[PeerEvaluation]) -> Dict:
        if not evaluations:
            return {
                "status": "No Data",
                "badge_color": "gray",
                "avg_score": 0.0,
                "variance": 0.0,
                "flag": False,
                "msg": "No evaluations submitted yet for this team.",
                "recommendation": "Encourage group members to complete peer reviews before the deadline.",
                "freeloaders": []
            }

        scores = [e.average_score for e in evaluations]
        avg_score = sum(scores) / len(scores)

        # Variance calculation (Sample Variance)
        if len(scores) > 1:
            variance = sum((x - avg_score) ** 2 for x in scores) / (len(scores) - 1)
        else:
            variance = 0.0

        # Detect potential freeloading per evaluatee
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

        has_flag = (variance > self.variance_threshold) or (len(freeloaders) > 0) or (avg_score < self.low_score_threshold)

        if len(freeloaders) > 0:
            status = "Critical Conflict"
            badge_color = "red"
            msg = f"Potential freeloading detected ({len(freeloaders)} member(s) scored below threshold)."
            recommendation = "Schedule an immediate team check-in to reassign tasks and review member contributions."
        elif variance > self.variance_threshold:
            status = "Warning"
            badge_color = "orange"
            msg = "High score variance detected across peer evaluations."
            recommendation = "Review individual qualitative feedback to identify communication bottlenecks."
        else:
            status = "Healthy"
            badge_color = "green"
            msg = "Group evaluation scores indicate balanced team contribution."
            recommendation = "Team collaboration is optimal. Proceed with standard monitoring."

        return {
            "status": status,
            "badge_color": badge_color,
            "avg_score": round(avg_score, 2),
            "variance": round(variance, 2),
            "flag": has_flag,
            "msg": msg,
            "recommendation": recommendation,
            "freeloaders": freeloaders
        }


class DataStorage:
    FILE_PATH = "data_store.json"

    @classmethod
    def save_evaluations(cls, evaluations: List[PeerEvaluation]):
        data = [asdict(e) for e in evaluations]
        with open(cls.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_evaluations(cls) -> List[PeerEvaluation]:
        if not os.path.exists(cls.FILE_PATH):
            return []
        try:
            with open(cls.FILE_PATH, "r") as f:
                data = json.load(f)
                return [PeerEvaluation(**item) for item in data]
        except Exception:
            return []