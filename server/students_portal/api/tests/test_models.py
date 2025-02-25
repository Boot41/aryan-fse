from django.test import TestCase
from api.models import User, Subject, Assignment, StudentAssignment
from django.utils import timezone

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123",
            role="student"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.name, "Test User")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.role, "student")

    def test_user_str_representation(self):
        self.assertEqual(str(self.user), "test@example.com")

class SubjectModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Mathematics",
            description="Mathematics subject"
        )

    def test_subject_creation(self):
        self.assertEqual(self.subject.name, "Mathematics")
        self.assertEqual(self.subject.description, "Mathematics subject")

    def test_subject_str_representation(self):
        self.assertEqual(str(self.subject), "Mathematics")

class AssignmentModelTest(TestCase):
    def setUp(self):
        self.subject = Subject.objects.create(
            name="Mathematics",
            description="Mathematics subject"
        )
        self.assignment = Assignment.objects.create(
            title="Math Test",
            description="Test description",
            subject=self.subject,
            topic="Algebra",
            questions={"q1": "What is 2+2?"}
        )

    def test_assignment_creation(self):
        self.assertEqual(self.assignment.title, "Math Test")
        self.assertEqual(self.assignment.subject, self.subject)
        self.assertEqual(self.assignment.topic, "Algebra")
        self.assertEqual(self.assignment.questions, {"q1": "What is 2+2?"})

    def test_assignment_str_representation(self):
        self.assertEqual(str(self.assignment), "Math Test")

class StudentAssignmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            name="Test Student",
            email="student@example.com",
            password="testpass123",
            role="student"
        )
        self.subject = Subject.objects.create(
            name="Mathematics",
            description="Mathematics subject"
        )
        self.assignment = Assignment.objects.create(
            title="Math Test",
            description="Test description",
            subject=self.subject,
            topic="Algebra",
            questions={"q1": "What is 2+2?"}
        )
        self.student_assignment = StudentAssignment.objects.create(
            student=self.user,
            assignment=self.assignment,
            answers={"q1": "4"},
            status="completed",
            score=100
        )

    def test_student_assignment_creation(self):
        self.assertEqual(self.student_assignment.student, self.user)
        self.assertEqual(self.student_assignment.assignment, self.assignment)
        self.assertEqual(self.student_assignment.answers, {"q1": "4"})
        self.assertEqual(self.student_assignment.status, "completed")
        self.assertEqual(self.student_assignment.score, 100)

    def test_student_assignment_str_representation(self):
        expected = f"{self.user.name} - {self.assignment.title}"
        self.assertEqual(str(self.student_assignment), expected)
