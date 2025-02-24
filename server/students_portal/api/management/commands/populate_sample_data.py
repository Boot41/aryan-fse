from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import User, Subject, Assignment, StudentAssignment
from datetime import datetime, timedelta
import json
import random

class Command(BaseCommand):
    help = 'Populates the database with sample data for testing'

    def handle(self, *args, **kwargs):
        # Check if database is empty
        if User.objects.exists():
            self.stdout.write(self.style.WARNING('Database is not empty. Skipping sample data creation.'))
            return

        try:
            with transaction.atomic():
                self.stdout.write('Creating sample data...')
                
                # Create users with different roles
                users = self._create_users()
                self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))
                
                # Create subjects
                subjects = self._create_subjects()
                self.stdout.write(self.style.SUCCESS(f'Created {len(subjects)} subjects'))
                
                # Create assignments
                assignments = self._create_assignments(subjects)
                self.stdout.write(self.style.SUCCESS(f'Created {len(assignments)} assignments'))
                
                # Create student assignments
                student_assignments = self._create_student_assignments(users, assignments)
                self.stdout.write(self.style.SUCCESS(f'Created {len(student_assignments)} student assignments'))

                self.stdout.write(self.style.SUCCESS('Successfully created all sample data'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating sample data: {str(e)}'))
            raise e

    def _create_users(self):
        users = []
        
        # Create admin
        admin = User.objects.create(
            name='Admin User',
            email='admin@example.com',
            password='admin123',
            role='admin'
        )
        users.append(admin)
        
        # Create teachers
        teacher_names = ['Dr. Sarah Johnson', 'Prof. Michael Chen', 'Dr. Emily Brown']
        for i, name in enumerate(teacher_names):
            email = f'teacher{i+1}@example.com'
            users.append(User.objects.create(
                name=name,
                email=email,
                password='teacher123',
                role='teacher'
            ))
        
        # Create students
        student_first_names = ['Alex', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Sam', 'Jamie', 'Riley']
        student_last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        
        for i in range(15):
            first_name = random.choice(student_first_names)
            last_name = random.choice(student_last_names)
            name = f'{first_name} {last_name}'
            email = f'student{i+1}@example.com'
            users.append(User.objects.create(
                name=name,
                email=email,
                password='student123',
                role='student'
            ))
        
        return users

    def _create_subjects(self):
        subjects_data = [
            {
                'name': 'Advanced Mathematics',
                'description': 'Complex mathematical concepts including calculus, linear algebra, and statistics'
            },
            {
                'name': 'Computer Science Fundamentals',
                'description': 'Core concepts of computer science including algorithms, data structures, and programming paradigms'
            },
            {
                'name': 'Physics',
                'description': 'Study of matter, energy, and their interactions'
            },
            {
                'name': 'Database Systems',
                'description': 'Design and implementation of database systems, SQL, and data modeling'
            }
        ]
        
        return [Subject.objects.create(**subject) for subject in subjects_data]

    def _create_assignments(self, subjects):
        assignments = []
        assignment_data = [
            {
                'title': 'Linear Algebra Problem Set',
                'description': 'Solve problems related to vector spaces and linear transformations',
                'questions': json.dumps([
                    {'question': 'Define vector space', 'points': 10},
                    {'question': 'Prove that the set of all polynomials is a vector space', 'points': 20},
                    {'question': 'Find the eigenvalues of a given matrix', 'points': 20}
                ]),
                'duration': 90,  # 1.5 hours
                'total_questions': 3
            },
            {
                'title': 'Database Design Project',
                'description': 'Design a database schema for a university management system',
                'questions': json.dumps([
                    {'question': 'Identify the main entities', 'points': 10},
                    {'question': 'Create an ER diagram', 'points': 20},
                    {'question': 'Implement the schema in SQL', 'points': 30}
                ]),
                'duration': 120,  # 2 hours
                'total_questions': 3
            },
            {
                'title': 'Physics Lab Report',
                'description': 'Write a report on the pendulum experiment',
                'questions': json.dumps([
                    {'question': 'Describe the experimental setup', 'points': 10},
                    {'question': 'Analyze the results', 'points': 20},
                    {'question': 'Discuss sources of error', 'points': 10}
                ]),
                'duration': 60,  # 1 hour
                'total_questions': 3
            }
        ]

        for data in assignment_data:
            assignment = Assignment.objects.create(
                title=data['title'],
                description=data['description'],
                questions=data['questions'],
                subject=random.choice(subjects),
                duration=data['duration'],
                total_questions=data['total_questions']
            )
            assignments.append(assignment)
        return assignments

    def _create_student_assignments(self, users, assignments):
        student_assignments = []
        students = [user for user in users if user.role == 'student']
        statuses = ['pending', 'completed']

        for student in students:
            for assignment in assignments:
                status = random.choice(statuses)
                score = random.randint(50, 100) if status == 'completed' else None
                submission = f'Submission by {student.name}' if status == 'completed' else None

                student_assignment = StudentAssignment.objects.create(
                    student=student,
                    assignment=assignment,
                    status=status,
                    score=score,
                    submission=submission,
                    submitted_at=datetime.now() if status == 'completed' else None,
                    graded_at=datetime.now() if status == 'completed' else None
                )
                student_assignments.append(student_assignment)
        return student_assignments
