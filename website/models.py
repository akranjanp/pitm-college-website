from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200, help_text="e.g., Bachelor of Computer Applications")
    code = models.CharField(max_length=20, unique=True, help_text="e.g., BCA")
    description = models.TextField()
    duration_years = models.PositiveIntegerField(default=3, help_text="Duration of course in years")
    eligibility = models.CharField(max_length=300, help_text="e.g., 10+2 with Mathematics/CS or equivalent with 45% marks")
    seats = models.PositiveIntegerField(default=60)
    image = models.ImageField(upload_to='courses/', blank=True, null=True, help_text="Upload course cover image")

    def __str__(self):
        return f"{self.title} ({self.code})"

class Notice(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Show this notice on the notice board")
    is_urgent = models.BooleanField(default=False, help_text="Highlight notice in red/marquee")

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('campus', 'Campus Infrastructure'),
        ('labs', 'Labs & Library'),
        ('events', 'Events & Seminars'),
        ('sports', 'Sports & Activities'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='gallery/', help_text="Upload gallery image")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='campus')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_category_display()})"

class FacultyMember(models.Model):
    name = models.CharField(max_length=150)
    designation = models.CharField(max_length=150, help_text="e.g., Assistant Professor, HOD")
    department = models.CharField(max_length=150, help_text="e.g., Computer Science, Management")
    qualification = models.CharField(max_length=250, help_text="e.g., Ph.D, M.Tech, MBA")
    image = models.ImageField(upload_to='faculty/', blank=True, null=True, help_text="Upload faculty passport size photo")

    def __str__(self):
        return f"{self.name} - {self.designation} ({self.department})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Inquiry from {self.name} - {self.subject} ({self.submitted_at.strftime('%d-%m-%Y %H:%M')})"

class CarouselSlide(models.Model):
    title = models.CharField(max_length=200, help_text="Main heading on the slide")
    tag = models.CharField(max_length=50, blank=True, help_text="e.g., Admissions 2026 Open")
    description = models.TextField(blank=True, help_text="Subtitle description text")
    image = models.ImageField(upload_to='carousel/', help_text="Upload background banner image")
    button_text = models.CharField(max_length=50, default="Know More")
    button_link = models.CharField(max_length=200, default="/courses/")
    order = models.PositiveIntegerField(default=0, help_text="Display order (ascending)")
    is_active = models.BooleanField(default=True, help_text="Tick to display on homepage")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
