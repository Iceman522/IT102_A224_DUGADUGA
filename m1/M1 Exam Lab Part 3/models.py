class User:
    def __init__(self, user_id: str, name: str, role: str):
        self._user_id = user_id
        self._name = name
        self._role = role

    def get_id(self) -> str:
        return self._user_id

    def get_name(self) -> str:
        return self._name

    def get_role(self) -> str:
        return self._role


class Student(User):
    def __init__(self, user_id: str, name: str, group_id: str):
        super().__init__(user_id, name, role="Student")
        self.group_id = group_id


class Instructor(User):
    def __init__(self, user_id: str, name: str, department: str):
        super().__init__(user_id, name, role="Instructor")
        self.department = department


class ProjectGroup:
    def __init__(self, group_id: str, group_name: str, members: list[str]):
        self.group_id = group_id
        self.group_name = group_name
        self.members = members


class PeerEvaluation:
    def __init__(self, evaluator_id: str, evaluatee_id: str, score: int, comments: str):
        self.evaluator_id = evaluator_id
        self.evaluatee_id = evaluatee_id
        self.score = score
        self.comments = comments


class SystemManager:
    def __init__(self):
        # Simulated database records
        self.students = {
            "S101": Student("S101", "Adrian Dugaduga", "G-01"),
            "S102": Student("S102", "Maria Santos", "G-01"),
            "S103": Student("S103", "John Doe", "G-01")
        }
        self.instructors = {
            "I201": Instructor("I201", "Prof. Alexander Reyes", "Information Systems")
        }
        self.groups = {
            "G-01": ProjectGroup("G-01", "Group 1 - Systems Architecture", ["S101", "S102", "S103"])
        }
        self.evaluations = []

    def authenticate(self, user_id: str, role: str) -> User | None:
        if role == "Student":
            return self.students.get(user_id)
        elif role == "Instructor":
            return self.instructors.get(user_id)
        return None

    def get_group(self, group_id: str) -> ProjectGroup | None:
        return self.groups.get(group_id)

    def submit_evaluation(self, eval_obj: PeerEvaluation):
        self.evaluations.append(eval_obj)