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
                    {
                        'id': 1,
                        'question': 'Which of the following is a property of vector spaces?',
                        'options': [
                            'Closure under multiplication only',
                            'Closure under addition and multiplication',
                            'No identity element',
                            'No inverse elements'
                        ],
                        'correctAnswer': 'Closure under addition and multiplication',
                        'points': 10
                    },
                    {
                        'id': 2,
                        'question': 'What is the rank of a 3x3 identity matrix?',
                        'options': ['1', '2', '3', '4'],
                        'correctAnswer': '3',
                        'points': 20
                    },
                    {
                        'id': 3,
                        'question': 'If a matrix has eigenvalues 2, 3, and 5, what is its trace?',
                        'options': ['6', '8', '10', '30'],
                        'correctAnswer': '10',
                        'points': 20
                    }
                ]),
                'duration': 90,  # 1.5 hours
                'total_questions': 3
            },
            {
                'title': 'Database Design Project',
                'description': 'Design a database schema for a university management system',
                'questions': json.dumps([
                    {
                        'id': 1,
                        'question': 'Which relationship type represents "A student can enroll in many courses and a course can have many students"?',
                        'options': [
                            'One-to-One',
                            'One-to-Many',
                            'Many-to-Many',
                            'None of the above'
                        ],
                        'correctAnswer': 'Many-to-Many',
                        'points': 10
                    },
                    {
                        'id': 2,
                        'question': 'What is normalization in database design?',
                        'options': [
                            'Process of creating tables',
                            'Process of organizing data to reduce redundancy',
                            'Process of adding more data',
                            'Process of deleting data'
                        ],
                        'correctAnswer': 'Process of organizing data to reduce redundancy',
                        'points': 20
                    },
                    {
                        'id': 3,
                        'question': 'Which SQL statement is used to create a new table?',
                        'options': [
                            'NEW TABLE',
                            'CREATE TABLE',
                            'ADD TABLE',
                            'INSERT TABLE'
                        ],
                        'correctAnswer': 'CREATE TABLE',
                        'points': 30
                    }
                ]),
                'duration': 120,  # 2 hours
                'total_questions': 3
            },
            {
                'title': 'Physics Lab Report',
                'description': 'Write a report on the pendulum experiment',
                'questions': json.dumps([
                    {
                        'id': 1,
                        'question': 'What affects the period of a simple pendulum?',
                        'options': [
                            'Mass of the bob',
                            'Length of the string',
                            'Initial displacement',
                            'Color of the bob'
                        ],
                        'correctAnswer': 'Length of the string',
                        'points': 10
                    },
                    {
                        'id': 2,
                        'question': 'The period of a pendulum is doubled. What happened to its length?',
                        'options': [
                            'Doubled',
                            'Quadrupled',
                            'Halved',
                            'Remained the same'
                        ],
                        'correctAnswer': 'Quadrupled',
                        'points': 20
                    },
                    {
                        'id': 3,
                        'question': 'Which force is responsible for the pendulum\'s motion?',
                        'options': [
                            'Electric force',
                            'Magnetic force',
                            'Gravitational force',
                            'Nuclear force'
                        ],
                        'correctAnswer': 'Gravitational force',
                        'points': 10
                    }
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
