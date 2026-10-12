import unittest
from models import Student, PeerEvaluation, GroupHealthAnalyzer

class TestPeerEvalDSS(unittest.TestCase):
    
    def setUp(self):
        """Set up standard test fixtures before each test."""
        self.analyzer = GroupHealthAnalyzer(variance_threshold=1.2, low_score_threshold=2.5)
        self.members = [
            Student(user_id="S1", name="Alice", role="Student", group_id="G1"),
            Student(user_id="S2", name="Bob", role="Student", group_id="G1"),
            Student(user_id="S3", name="Charlie", role="Student", group_id="G1")
        ]

    def test_empty_evaluations_edge_case(self):
        """Test edge case where no evaluations have been submitted yet."""
        result = self.analyzer.analyze_health(self.members, [])
        self.assertEqual(result["status"], "No Data")
        self.assertFalse(result["flag"])
        self.assertEqual(result["avg_score"], 0.0)
        self.assertEqual(result["variance"], 0.0)

    def test_single_evaluation_edge_case(self):
        """Test edge case with only 1 review to ensure sigma calculation doesn't throw division-by-zero."""
        single_eval = [
            PeerEvaluation("e1", "S1", "S2", 4, 4, 4, "Good work.")
        ]
        result = self.analyzer.analyze_health(self.members, single_eval)
        self.assertEqual(result["sigma"], 0.0)
        self.assertEqual(result["avg_score"], 4.0)

    def test_freeloading_detection(self):
        """Test that low-scoring outliers are correctly flagged as freeloaders."""
        evaluations = [
            PeerEvaluation("e1", "S1", "S3", 1, 1, 1, "Did not contribute."),
            PeerEvaluation("e2", "S2", "S3", 2, 1, 2, "Unresponsive."),
            PeerEvaluation("e3", "S3", "S1", 5, 5, 5, "Great leader.")
        ]
        result = self.analyzer.analyze_health(self.members, evaluations)
        self.assertTrue(result["flag"])
        self.assertEqual(result["status"], "Critical Conflict")
        self.assertIn("S3", result["freeloaders"])

    def test_healthy_synergy(self):
        """Test a team with uniformly high scores and low variance."""
        evaluations = [
            PeerEvaluation("e1", "S1", "S2", 5, 5, 5, "Excellent."),
            PeerEvaluation("e2", "S2", "S3", 4, 5, 5, "Solid output."),
            PeerEvaluation("e3", "S3", "S1", 5, 4, 5, "Reliable teammate.")
        ]
        result = self.analyzer.analyze_health(self.members, evaluations)
        self.assertEqual(result["status"], "Healthy")
        self.assertFalse(result["flag"])
        self.assertEqual(len(result["freeloaders"]), 0)

if __name__ == "__main__":
    unittest.main()