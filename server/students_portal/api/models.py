from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, role='admin', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, role, password, **extra_fields)

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Storing password directly
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'role']

    def __str__(self):
        return self.email

    def authenticate(self, password):
        return self.password == password

# Subject model
class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Assignment model
class Assignment(models.Model):
    ASSIGNMENT_TYPE_CHOICES = [
        ('general', 'General'),
        ('special', 'Special'),
    ]
    
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    questions = models.JSONField(help_text="JSON array of questions related to the topic")
    assignment_type = models.CharField(max_length=20, choices=ASSIGNMENT_TYPE_CHOICES)
    duration = models.IntegerField(help_text="Duration of the assignment in minutes", default=60)
    total_questions = models.IntegerField(help_text="Total number of questions", default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.subject.name}"

# StudentAssignment model for mapping assignments to students
class StudentAssignment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_assignments')
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='student_assignments')
    status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ])
    submission = models.JSONField(null=True, blank=True, help_text="JSON containing student's answers")
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    graded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.assignment.title}"
