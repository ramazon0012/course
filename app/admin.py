from django.contrib import admin
from app.models import Course, Part, User, Rating, Review, Comment, Lecture, Video, Tags
# Register your models here.
admin.site.register(Part)
admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(Lecture)
admin.site.register(Video)
admin.site.register(Tags)