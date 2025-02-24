from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import User, Subject, Enrollment, Assessment, ChatbotInteraction, SubjectTeacher, TeacherStudentMapping
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with dummy data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting to populate database...')
        
        try:
            with transaction.atomic():
                # Create admin user
                admin = User.objects.create_superuser(
                    email='admin@example.com',
                    name='Admin User',
                    password='admin123'
                )
                self.stdout.write(self.style.SUCCESS('Created admin user'))

                # Create teachers
                teachers = []
                for i in range(3):
                    teacher = User.objects.create_user(
                        email=f'teacher{i+1}@example.com',
                        name=f'Teacher {i+1}',
                        role='teacher',
                        password='teacher123'
                    )
                    teachers.append(teacher)
                self.stdout.write(self.style.SUCCESS('Created teachers'))

                # Create students
                students = []
                for i in range(10):
                    student = User.objects.create_user(
                        email=f'student{i+1}@example.com',
                        name=f'Student {i+1}',
                        role='student',
                        password='student123'
                    )
                    students.append(student)
                self.stdout.write(self.style.SUCCESS('Created students'))

                # Create subjects
                subjects = []
                subject_names = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science']
                for name in subject_names:
                    subject = Subject.objects.create(
                        name=name,
                        description=f'This is {name} course',
                        course_handout='https://example.com/handout.pdf'
                    )
                    subjects.append(subject)
                self.stdout.write(self.style.SUCCESS('Created subjects'))

                # Create subject-teacher mappings
                for subject in subjects:
                    teacher = random.choice(teachers)
                    SubjectTeacher.objects.create(
                        teacher=teacher,
                        subject=subject
                    )
                self.stdout.write(self.style.SUCCESS('Created subject-teacher mappings'))

                # Create enrollments and teacher-student mappings
                for student in students:
                    # Enroll each student in 2-4 random subjects
                    chosen_subjects = random.sample(subjects, random.randint(2, 4))
                    for subject in chosen_subjects:
                        # Create enrollment
                        Enrollment.objects.create(
                            user=student,
                            subject=subject,
                            score=random.uniform(60.0, 100.0)
                        )
                        
                        # Get the teacher for this subject
                        subject_teacher = SubjectTeacher.objects.filter(subject=subject).first()
                        if subject_teacher:
                            TeacherStudentMapping.objects.create(
                                teacher=subject_teacher.teacher,
                                student=student,
                                subject=subject
                            )
                self.stdout.write(self.style.SUCCESS('Created enrollments and teacher-student mappings'))

                # Create some assessments
                for student in students:
                    enrollments = Enrollment.objects.filter(user=student)
                    for enrollment in enrollments:
                        Assessment.objects.create(
                            student=student,
                            subject=enrollment.subject,
                            teacher=SubjectTeacher.objects.filter(subject=enrollment.subject).first().teacher,
                            test_data={
                                'questions': [
                                    {'question': 'Sample question 1?', 'answer': 'Sample answer 1'},
                                    {'question': 'Sample question 2?', 'answer': 'Sample answer 2'}
                                ]
                            },
                            result=random.uniform(60.0, 100.0)
                        )
                self.stdout.write(self.style.SUCCESS('Created assessments'))

                # Create some chatbot interactions
                for student in students:
                    enrollments = Enrollment.objects.filter(user=student)
                    for enrollment in enrollments:
                        ChatbotInteraction.objects.create(
                            student=student,
                            subject=enrollment.subject,
                            message='Can you explain this concept?',
                            response='Here is the explanation...'
                        )
                self.stdout.write(self.style.SUCCESS('Created chatbot interactions'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
            raise e

        self.stdout.write(self.style.SUCCESS('Successfully populated database'))
