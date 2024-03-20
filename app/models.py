from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here

class User(AbstractUser):
    TEACHER = 'teacher'
    STUDENT = 'student'
    USER_TYPES = [
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=STUDENT)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=50)
    avatar = models.ImageField(null=True, blank=True, upload_to="avatar/")
    follower = models.ManyToManyField('User', related_name='follow', blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def delete_self(self):
        self.delete()

    def is_teacher(self):
        return self.user_type == self.TEACHER

    def is_student(self):
        return self.user_type == self.STUDENT


class Part(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=15)
    
    def __str__(self) -> str:
        return self.name
    
    def get_course_count(self):
        return self.parts.count()
    
    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])

class Course(models.Model):
    reatings = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    name = models.CharField(max_length=50)
    students = models.ManyToManyField(User, related_name="student", blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher")
    like = models.ManyToManyField(User, related_name = 'like', blank=True)
    image = models.ImageField(upload_to="media/")
    body = models.TextField()
    level = models.CharField(max_length=15)
    price = models.IntegerField()
    part = models.ForeignKey(Part, related_name='parts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)
    
    def get_ratings(self):
        return Rating.objects.filter(course=self)

    def get_number_of_students(self):
        student_count = self.students.count()
        total_students = student_count 

        return total_students
    
    def calculate_average_rating(self):
        user_ratings = [int(rating.rating) for rating in self.get_ratings()]
        if user_ratings:
            return sum(user_ratings) / len(user_ratings)
        else:
            return 0    
        
    def get_average_rating_as_stars(self):
        average_rating = self.calculate_average_rating()
        full_stars = int(average_rating)
        half_stars = 1 if average_rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_stars

        stars_html = '⭐' * full_stars + '½' * half_stars + '☆' * empty_stars
        return stars_html
    
    def __str__(self) -> str:
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name = 'likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)

    def get_all_user_ratings(self):
        return Rating.objects.filter(course=self.course)

    def calculate_all_users_average_rating(self):
        all_user_ratings = [int(rating.rating) for rating in self.get_all_user_ratings()]
        if all_user_ratings:
            return sum(all_user_ratings) / len(all_user_ratings)
        else:
            return 0
    def get_all_users_ratings_as_stars(self):
        user_ratings = self.rating_set.all()  

        stars_list = []
        for rating in user_ratings:
            full_stars = int(rating.rating)
            half_stars = 1 if rating.rating - full_stars >= 0.5 else 0
            empty_stars = 5 - full_stars - half_stars

            stars_html = '⭐' * full_stars + '½' * half_stars + '☆' * empty_stars
            stars_list.append(stars_html)

        return stars_list

        
    class Meta:
        ordering = ['-upload_at', '-created_at']

    def __str__(self):
        return str(self.body)
 
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.IntegerField(choices=Course.reatings, default='1')
    
    def get_rating_as_stars(self):
        full_stars = int(self.rating)
        half_stars = 1 if self.rating - full_stars >= 0.5 else 0
        empty_stars = 5 - full_stars - half_stars

        stars_html = '⭐' * full_stars + '½' * half_stars + '☆' * empty_stars
        return stars_html

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name = 'likelar', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    upload_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-upload_at', '-created_at']


    @property
    def getReplies(self):
        return Comment.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        
    def __str__(self):
        return str(self.body)
    
class Lecture(models.Model):
    name = models.CharField(max_length=50)
    videos = models.ManyToManyField('Video', related_name='videos')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='lectures', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def videos_watched_percentage(self):
        total_videos = self.videos.count()  # Use self.videos instead of self.video_set
        watched_videos = self.videos.filter(watched=True).count()

        if total_videos > 0:
            percentage = (watched_videos / total_videos) * 100
            return round(percentage, 2)
        else:
            return 0
    
    def video_fraction(self):
        total_videos = self.videos.count()
        watched_videos = self.videos.filter(watched=True).count()

        if total_videos > 0:
            percentage = watched_videos / total_videos
            return round(percentage, 2)
        else:
            return 0
    
class Video(models.Model):
    file = models.FileField(upload_to="videos/")
    video_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=44)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to="posters/")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
    last_watched = models.DateTimeField(null=True, blank=True)
    watched = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.last_watched:
            self.watched = True
            self.last_watched = timezone.now()
        super(Video, self).save(*args, **kwargs)

class Tags(models.Model):
    name = models.CharField(max_length=25)
    course = models.ForeignKey(Course, related_name='courslar', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name