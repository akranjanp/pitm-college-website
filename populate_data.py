import os
import sys
from datetime import datetime

# Initialize Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'patna_college.settings')

import django
django.setup()

from django.core.files import File
from website.models import Course, Notice, GalleryImage, FacultyMember, ContactMessage, CarouselSlide

# Check if PIL (Pillow) is available to draw placeholder images
try:
    from PIL import Image, ImageDraw
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

def create_media_directories():
    os.makedirs('media/courses', exist_ok=True)
    os.makedirs('media/gallery', exist_ok=True)
    os.makedirs('media/faculty', exist_ok=True)
    os.makedirs('media/carousel', exist_ok=True)


def generate_placeholder_image(filename, text, size=(600, 400), bg_color=(30, 58, 138), fg_color=(234, 179, 8)):
    """Generates a professional solid color placeholder image with custom text"""
    create_media_directories()
    filepath = os.path.join('media', filename)
    
    if HAS_PILLOW:
        img = Image.new('RGB', size, color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Simple geometric pattern to make it look nicer
        draw.rectangle([10, 10, size[0]-10, size[1]-10], outline=fg_color, width=2)
        draw.line([10, 10, size[0]-10, size[1]-10], fill=(255, 255, 255, 50), width=1)
        draw.line([10, size[1]-10, size[0]-10, 10], fill=(255, 255, 255, 50), width=1)
        
        # Draw text (centered simply)
        draw.text((30, size[1] // 2 - 10), text, fill=fg_color)
        
        img.save(filepath, 'JPEG')
    else:
        # Create a dummy blank file if Pillow is not active
        with open(filepath, 'wb') as f:
            f.write(b'\x00' * 1024)
            
    return filepath

def populate_database():
    print("Clearing existing data...")
    Course.objects.all().delete()
    Notice.objects.all().delete()
    GalleryImage.objects.all().delete()
    FacultyMember.objects.all().delete()
    ContactMessage.objects.all().delete()
    CarouselSlide.objects.all().delete()
    
    print("Generating media placeholder images...")
    img_slide1 = generate_placeholder_image('carousel/slide1.jpg', 'Slide 1: PITM Campus Banner', (1200, 600))
    img_slide2 = generate_placeholder_image('carousel/slide2.jpg', 'Slide 2: Advanced Labs', (1200, 600))
    img_slide3 = generate_placeholder_image('carousel/slide3.jpg', 'Slide 3: Placements Support', (1200, 600))

    img_bca = generate_placeholder_image('courses/bca.jpg', 'BCA - Computer Applications')
    img_bba = generate_placeholder_image('courses/bba.jpg', 'BBA - Business Administration')
    img_bscit = generate_placeholder_image('courses/bscit.jpg', 'B.Sc. IT - Information Technology')
    img_bcom = generate_placeholder_image('courses/bcom.jpg', 'B.Com - Commerce (Hons)')
    
    img_f1 = generate_placeholder_image('faculty/prof_verma.jpg', 'Prof. R.K. Verma - CSE', (300, 300), (15, 23, 42), (255, 255, 255))
    img_f2 = generate_placeholder_image('faculty/dr_prasad.jpg', 'Dr. Anjali Prasad - MBA', (300, 300), (15, 23, 42), (255, 255, 255))
    img_f3 = generate_placeholder_image('faculty/mr_kumar.jpg', 'Mr. Amit Kumar - IT', (300, 300), (15, 23, 42), (255, 255, 255))
    img_f4 = generate_placeholder_image('faculty/mrs_sharma.jpg', 'Mrs. Neha Sharma - BCom', (300, 300), (15, 23, 42), (255, 255, 255))
    
    img_g1 = generate_placeholder_image('gallery/campus_front.jpg', 'PITM Campus Frontage', (800, 600))
    img_g2 = generate_placeholder_image('gallery/comp_lab.jpg', 'High-Speed Computing Lab', (800, 600))
    img_g3 = generate_placeholder_image('gallery/library.jpg', 'Central Library Reading Hall', (800, 600))
    img_g4 = generate_placeholder_image('gallery/seminar.jpg', 'Tech Seminar Room 1', (800, 600))
    img_g5 = generate_placeholder_image('gallery/sports.jpg', 'Annual Athletics Arena', (800, 600))
    img_g6 = generate_placeholder_image('gallery/convocation.jpg', 'Graduation Ceremony 2025', (800, 600))

    print("Adding Courses...")
    c1 = Course.objects.create(
        title="Bachelor of Computer Applications",
        code="BCA",
        description="A premier three-year undergraduate program focusing on computational structures, systems design, software development, database administration, and web engineering. This program equips students with modern programming skills in Java, Python, C++, and database management systems (DBMS), paving the path for roles like Systems Analyst, Software Engineer, or Database Administrator.",
        duration_years=3,
        eligibility="Passed 10+2 (Intermediate) examination in Arts, Science, or Commerce stream with Mathematics or Computer Science as one of the subjects, securing at least 45% marks in aggregate.",
        seats=60
    )
    c1.image.name = 'courses/bca.jpg'
    c1.save()

    c2 = Course.objects.create(
        title="Bachelor of Business Administration",
        code="BBA",
        description="A modern three-year undergraduate program training students in business fundamentals, marketing, financial accounting, human resource operations, and corporate communications. The course includes interactive workshops, company visits, case studies, and business planning models to prepare young minds for corporate leadership positions or entrepreneurship.",
        duration_years=3,
        eligibility="Passed 10+2 (Intermediate) examination in any stream (Arts, Science, or Commerce) from a recognized board, securing at least 45% marks in aggregate.",
        seats=60
    )
    c2.image.name = 'courses/bba.jpg'
    c2.save()

    c3 = Course.objects.create(
        title="Bachelor of Science in Information Technology",
        code="B.Sc. IT",
        description="An industry-aligned undergraduate program centering on networking protocols, computer hardware architecture, cloud infrastructures, cybersecurity frameworks, and information systems. This course blends technical and theoretical expertise to support corporate system deployments.",
        duration_years=3,
        eligibility="Passed 10+2 (Intermediate) examination with Physics and Mathematics or Computer Science as primary subjects, securing at least 45% marks in aggregate.",
        seats=40
    )
    c3.image.name = 'courses/bscit.jpg'
    c3.save()

    c4 = Course.objects.create(
        title="Bachelor of Commerce (Hons)",
        code="B.Com",
        description="A professional degree course developing core expertise in financial auditing, taxation laws, corporate bookkeeping, economics, and corporate governance protocols. It establishes a strong foundation for students preparing for CA, CS, or MBA programs.",
        duration_years=3,
        eligibility="Passed 10+2 (Intermediate) in any stream, with preference to Commerce, securing at least 45% marks in aggregate.",
        seats=80
    )
    c4.image.name = 'courses/bcom.jpg'
    c4.save()

    print("Adding Notices...")
    Notice.objects.create(
        title="BCA & BBA Admissions Session 2026-29 Ongoing",
        content="Registrations for undergraduate admission to BCA, BBA, B.Sc. IT, and B.Com are active. Prospective students can submit their details via the contact form online or visit the campus admission desk directly. Last date to register is July 15th, 2026.",
        is_active=True,
        is_urgent=True
    )
    Notice.objects.create(
        title="Mid-Term Semester Examinations Schedule",
        content="The Mid-Term semester exams for BCA & BBA (Semesters II, IV, VI) are scheduled to commence from July 5th, 2026. The detailed day-wise timetable is published on the notice board outside the HOD office.",
        is_active=True,
        is_urgent=False
    )
    Notice.objects.create(
        title="Registrations Open for Annual Tech Hackathon 'PatnaHack'",
        content="PITM's annual tech hackathon 'PatnaHack 2026' is scheduled for August 12-13. Registrations are open for students from all departments. Prize pool includes cash awards and internship opportunities. Register by July 20th.",
        is_active=True,
        is_urgent=False
    )

    print("Adding Faculty Members...")
    f1 = FacultyMember.objects.create(
        name="Prof. R. K. Verma",
        designation="HOD & Associate Professor",
        department="Computer Science",
        qualification="Ph.D. in Computer Science, M.Tech (CSE)"
    )
    f1.image.name = 'faculty/prof_verma.jpg'
    f1.save()

    f2 = FacultyMember.objects.create(
        name="Dr. Anjali Prasad",
        designation="Associate Professor",
        department="Management Studies",
        qualification="Ph.D. in Business Administration, MBA"
    )
    f2.image.name = 'faculty/dr_prasad.jpg'
    f2.save()

    f3 = FacultyMember.objects.create(
        name="Mr. Amit Kumar",
        designation="Assistant Professor",
        department="Information Technology",
        qualification="M.Tech in IT, B.Tech (CSE)"
    )
    f3.image.name = 'faculty/mr_kumar.jpg'
    f3.save()

    f4 = FacultyMember.objects.create(
        name="Mrs. Neha Sharma",
        designation="Lecturer",
        department="Commerce",
        qualification="M.Com, UGC NET Qualified"
    )
    f4.image.name = 'faculty/mrs_sharma.jpg'
    f4.save()

    print("Adding Gallery Images...")
    g1 = GalleryImage.objects.create(title="Main Campus Frontage", category="campus")
    g1.image.name = 'gallery/campus_front.jpg'
    g1.save()

    g2 = GalleryImage.objects.create(title="High-Speed Computing Lab", category="labs")
    g2.image.name = 'gallery/comp_lab.jpg'
    g2.save()

    g3 = GalleryImage.objects.create(title="Central Library Reading Hall", category="labs")
    g3.image.name = 'gallery/library.jpg'
    g3.save()

    g4 = GalleryImage.objects.create(title="National Tech Seminar", category="events")
    g4.image.name = 'gallery/seminar.jpg'
    g4.save()

    g5 = GalleryImage.objects.create(title="Annual Athletics Arena", category="sports")
    g5.image.name = 'gallery/sports.jpg'
    g5.save()

    g6 = GalleryImage.objects.create(title="Convocation Ceremony 2025", category="events")
    g6.image.name = 'gallery/convocation.jpg'
    g6.save()

    print("Adding Mock Contact Submissions...")
    ContactMessage.objects.create(
        name="Ashish Ranjan",
        email="ashish@example.com",
        phone="9876543210",
        subject="BCA Admissions Enquiry",
        message="Hello admissions team,\n\nI want to seek admission to the BCA program for the session 2026-29. Could you please share details about the semester fees and whether standard installment options are available?",
        is_read=False
    )
    ContactMessage.objects.create(
        name="Vikram Singh",
        email="vikram@example.com",
        phone="9123456780",
        subject="BBA Course Details",
        message="Dear Sir/Madam,\n\nI would like to inquire about the eligibility criteria for the BBA program. Is there any entrance exam or is admission done on the basis of Intermediate percentage?",
        is_read=True
    )
    ContactMessage.objects.create(
        name="Neha Kumari",
        email="neha.k@example.com",
        phone="9000123456",
        subject="B.Sc. IT Syllabus and Affiliation",
        message="Hello, I wanted to know which university this college is affiliated to, and whether B.Sc. IT students get placement assistance. Please share the brochure.",
        is_read=False
    )
    ContactMessage.objects.create(
        name="Aarav Mehta",
        email="aarav@example.com",
        phone="9988776655",
        subject="Scholarship Policies Inquiry",
        message="Dear Team, I scored 89% in my 10+2 Board exams. Do you offer scholarships or fee concessions for meritorious students?",
        is_read=True
    )

    print("Adding Carousel Slides...")
    CarouselSlide.objects.create(
        title="Empowering Futures, Inspiring Academic Innovation",
        tag="Admissions 2026 Open",
        description="Join Patliputra Institute of Technology & Management, Patna's premier destination for BCA, BBA, B.Sc. IT, and modern career-oriented vocational programs.",
        image="carousel/slide1.jpg",
        button_text="Explore Programs",
        button_link="/courses/",
        order=1
    )
    CarouselSlide.objects.create(
        title="State-of-the-Art Labs & Global Resources",
        tag="Modern Infrastructure",
        description="Gain hands-on skills in our modern high-speed computer labs, digital learning libraries, and collaboration zones structured for standard industry alignments.",
        image="carousel/slide2.jpg",
        button_text="Take a Tour",
        button_link="/about/",
        order=2
    )
    CarouselSlide.objects.create(
        title="Launch Your Career with Top Global IT Leaders",
        tag="100% Placement Support",
        description="Our dedicated placement cell ensures top recruiting drives, grooming mock sessions, and summer internship packages for every undergraduate student.",
        image="carousel/slide3.jpg",
        button_text="Enquire Now",
        button_link="/contact/",
        order=3
    )

    print("\nData population completed successfully!")
    print(f"Courses: {Course.objects.count()}")
    print(f"Notices: {Notice.objects.count()}")
    print(f"Faculty Members: {FacultyMember.objects.count()}")
    print(f"Gallery Images: {GalleryImage.objects.count()}")
    print(f"Contact Messages: {ContactMessage.objects.count()}")
    print(f"Carousel Slides: {CarouselSlide.objects.count()}")

if __name__ == '__main__':
    populate_database()
