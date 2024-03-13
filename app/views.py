from django.shortcuts import render, redirect, get_object_or_404
from app.models import Course, Part, Comment, User, Lecture, Video, Tags, Review
from app.forms import RatingReviewForm, CommentForm, UserForm, MyUserCreationForm, LoginForm, CourseSearchForm
from django.db.models import Q
from django.contrib import messages
from moviepy.video.io.VideoFileClip import VideoFileClip
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext as _
import logging
import math
from django.utils import timezone
from django.http import HttpResponse

logger = logging.getLogger(__name__)

def home(request):
    text = _("Boshqa kurslar")
    gap = _("Featured Courses")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    des = _("Get inspired and discover something new today. Grow your skill with the most reliable online courses and certifications in marketing, information technology, programming, and data science.")
    find = _("Find your course")
    nimadir = _("Explore top picks of the week")
    search = _("Search")
    language = _("Language")
    corses = _("Courses")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    parts = Part.objects.all()
    courses = Course.objects.all()
    
    return render(request, "home.html", {
        "courses" : courses,
        "parts" : parts,
        "text" : text,
        "gap" : gap,
        "category" : categorys,
        "title" : title,
        "des" : des,
        "find" : find,
        "nimadir" : nimadir,
        "search" : search,
        "language" : language,
        "corses" : corses,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa
    })

def courses(request):
    courses = Course.objects.all()
    for course in courses:
        lectures = Lecture.objects.filter(course_id=course.id)
        count = lectures.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(courses, 4)
    text = _("Boshqa kurslar")
    categorys = _("Category")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    title = _("Barcha kurslar")
    parts = Part.objects.all()
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, "courses.html", {
        "courses" : courses,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
        "parts" : parts,
        "count" : count
    })

def detail(request, pk):
    course = get_object_or_404(Course, id=pk)
    reviews = course.review_set.all()
    lectures = Lecture.objects.filter(course=course)
    videos = Video.objects.filter(course=course)
    parts = Part.objects.all()
    tags = Tags.objects.filter(course=course)
    comments = course.comment_set.all()

    comment_form = CommentForm()
    try:
        last_viewed_video_instance = Video.objects.filter(user=request.user, course=course).latest('last_watched')
    except Video.DoesNotExist:
        first_lecture = lectures.first()
        if first_lecture:
            first_video = first_lecture.videos.first()
            last_viewed_video_instance = first_video
        else:
            last_viewed_video_instance = None
    
    rating_review_form = RatingReviewForm()

    if request.method == 'POST':
        rating_review_form = RatingReviewForm(request.POST)
        if 'review_rating_submit' in request.POST:
            rating = rating_review_form.cleaned_data['rating']
            body = rating_review_form.cleaned_data['body']

            review = Review(
                course=course,
                user=request.user,
                rating=rating,
                body=body,
            )
            review.save()
            messages.success(request, 'Review successfully created.')

        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None

                new_comment = Comment(body=body, user=request.user, course=course, parent=parent)
                new_comment.save()
    text = _("Boshqa kurslar")
    gap = _("Featured Courses")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    des = _("Get inspired and discover something new today. Grow your skill with the most reliable online courses and certifications in marketing, information technology, programming, and data science.")
    find = _("Find your course")
    nimadir = _("Explore top picks of the week")
    search = _("Search")
    language = _("Language")
    corses = _("Courses")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    video_durations = [] 
    for lecture in lectures:
        for video in lecture.videos.all():
            video_path = f'media/{video.file.url}'
            try:
                clip = VideoFileClip(video_path)
                duration_seconds = clip.duration
                clip.close()

                video_durations.append({
                    'video_name': video.name,
                    'duration_seconds': duration_seconds,
                    'duration_minutes': round(duration_seconds / 60)
                })

            except Exception as e:
                error_message = f"Error calculating duration for video {video.name}: {str(e)}"
                logger.error(error_message)
    return render(request, "detail.html", {
        "course": course, 
        "reviews": reviews, 
        "duration_message" : video_durations,
        'comment_form': comment_form,
        'lectures' : lectures,
        'videos' : videos,
        'last_viewed_video': last_viewed_video_instance,
        'tags' : tags,
        'comments' : comments,
        "parts" : parts,
        "text" : text,
        "gap" : gap,
        "category" : categorys,
        "title" : title,
        "des" : des,
        "find" : find,
        "nimadir" : nimadir,
        "search" : search,
        "language" : language,
        "corses" : corses,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa
        }
    )

def search(request):
    query = request.GET.get('query', '')
    form = CourseSearchForm(request.GET)

    courses = Course.objects.all()
    text = _("Boshqa kurslar")
    categorys = _("Category")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    title = _("Boshqa kurslar")

    # Form-based filtering
    if form.is_valid():
        category = form.cleaned_data.get('category')
        price_level = form.cleaned_data.get('price_level')
        skill_level = form.cleaned_data.get('skill_level')

        if category:
            courses = courses.filter(part__slug=category)

        if price_level:
            if price_level == 'Free':
                courses = courses.filter(price=0)
            elif price_level == 'Paid':
                courses = courses.exclude(price=0)

        if skill_level:
            courses = courses.filter(level=skill_level)

    # Query parameter-based filtering
    if query:
        courses = courses.filter(
            Q(name__icontains=query) | Q(level__icontains=query) | Q(price__icontains=query)
        )

    context = {
        'form': form,
        'query': query,
        'courses': courses,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
    }

    return render(request, 'courses.html', context)

@login_required(login_url='login')
def like_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    if pk:
        course.like.add(request.user)

        return redirect('/courses/')

    return render(request, 'courses.html')
# ______________________
@login_required(login_url='login')
def deslike_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    if pk:
        course.like.remove(request.user)

        return redirect('/courses/')

    return render(request, 'courses.html')

def full_search(request):
    quer = request.GET.get('quer', '')
    parts  = Part.objects.filter(Q(name__icontains=quer))
    courses  = Course.objects.filter(Q(name__icontains=quer) | Q(level__icontains=quer) | Q(price__icontains=quer))
    text = _("Boshqa kurslar")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    context = {
        'quer': quer,
        'courses': courses,
        'parts': parts,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title
    }

    return render(request, 'all.html', context)

@login_required(login_url='login')
def updateUser(request, pk):
    page = 'User Update'

    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/')  # Removed pk=pk
        else:
            # Display form errors instead of a generic message
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')

    return render(request, 'edit.html', {'form': form, 'page': page})

def account(request, pk):
    
    user = get_object_or_404(User, id=pk)
    courses_c = None  # Set an initial value
    if user.is_teacher():
        courses_c = Course.objects.filter(teacher=user)
    
    query = request.GET.get('query', '')
    courses = Course.objects.filter(Q(name__icontains=query) | Q(level__icontains=query) | Q(price__icontains=query))
    text = _("Boshqa kurslar")
    categorys = _("Category")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    title = _("Boshqa kurslar")
    
    return render(request, "user.html", {
        'courses': courses,
        'courses_c': courses_c,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
    })

def loginPage(request):
    page = 'Login'
    users = User.objects.filter(user_type='student')
    if request.user.is_authenticated:
        return redirect('/')  # Change the redirect URL as per your requirement

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'User does not exist')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('/')  # Change the redirect URL as per your requirement
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')

    else:
        form = LoginForm()

    context = {
        'form': form,
        'page': page,
        'users' : users,
    }
    return render(request, 'login.html', context)
#___________________
def logoutUser(request):
    logout(request)
    return redirect('/')
#___________________
def registerPage(request):
    page = 'Sign Up'
    users = User.objects.filter(user_type='student')
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            pass

    else:
        form = MyUserCreationForm()

    context = {
        'form': form,
        'page': page,
        'users' : users,
    }
    return render(request, 'register.html', context)

def coursesview(request, part_slug=None):
    part = None
    parts = Part.objects.all()
    text = _("Boshqa kurslar")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    courses = Course.objects.all()
    if part_slug:
        part = get_object_or_404(Part, 
        slug=part_slug)
    courses = courses.filter(part=part)
    return render(request,
        'courses.html',
        {'part': part,
        'parts': parts,
        'courses': courses,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
        })

def detail_video(request, pk, id):
    course = get_object_or_404(Course, id=pk)
    tags = Tags.objects.filter(course=course)
    reviews = course.review_set.all()
    lectures = Lecture.objects.filter(course=course)
    lecture = get_object_or_404(lectures, id=pk)
    videos_queryset = lecture.videos.all()

    if videos_queryset.exists():
        video_ids = videos_queryset.get(id=id)
    else:
        video_ids = None
    video = get_object_or_404(Video, id=id)
    video.last_watched = timezone.now()
    video.save()
    lecture_count = lectures.count()
    comments = course.comment_set.all()

    comment_form = CommentForm()
    text = _("Boshqa kurslar")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    video_durations = []
    for lecture in lectures:
        for video in lecture.videos.all():
            video_path = f'media/{video.file.url}'
            try:
                clip = VideoFileClip(video_path)
                duration_seconds = clip.duration
                clip.close()

                video_durations.append({
                    'video_name': video.name,
                    'duration_seconds': duration_seconds,
                    'duration_minutes': round(duration_seconds / 60)
                })

            except Exception as e:
                error_message = f"Error calculating duration for video {video.name}: {str(e)}"
                logger.error(error_message)
    rating_review_form = RatingReviewForm()

    if request.method == 'POST':
        rating_review_form = RatingReviewForm(request.POST)
        if rating_review_form.is_valid():
            rating = rating_review_form.cleaned_data['rating']
            body = rating_review_form.cleaned_data['body']

            review = Review(
                course=course,
                user=request.user,
                rating=rating,
                body=body,
            )
            review.save()
            messages.success(request, 'Review successfully created.')

        elif 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent = None

                new_comment = Comment(body=body, user=request.user, course=course, parent=parent)
                new_comment.save()

    return render(request, "video_detail.html", {
        "course": course, 
        "reviews": reviews, 
        'comment_form': comment_form,
        'lecture_count' : lecture_count,
        'lectures' : lectures,
        'tags' : tags,
        'lecture' : lecture,
        "duration_message" : video_durations,
        'comments' : comments,
        'video_ids' : video_ids,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title
        }
    )

def courses_tag(request, name):
    courses = Tags.objects.filter(name=name)
    for course in courses:
        lectures = Lecture.objects.filter(course_id=course.id)
        count = lectures.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(courses, 4)
    text = _("Boshqa kurslar")
    categorys = _("Category")
    title = _("Education, talents, and career opportunities. All in one place.")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    
    return render(request, 'courses_tag.html', {
        'courses' : courses,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
        "count" : count,
    })

def delete_course(request, pk, id):
    user = get_object_or_404(User, id=id)
    if pk:
        course = Course.objects.get(id=pk)
        course.delete()

        return redirect(request.META.get('HTTP_REFERER'))

    return render(request, 'user.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def delete_user(request, user_id):
    if user_id is not None:
        user = get_object_or_404(User, id=user_id)

        # Check if the user making the request is either a staff member or the user they are trying to delete
        if request.user.is_staff or request.user == user:
            user.delete()

        # Use a default URL in case HTTP_REFERER is not present
        return redirect('/')

    return render(request, 'delete_user.html')

def user_courses(request, pk):
    user = get_object_or_404(User, id=pk)
    user_courses = None  # Set an initial value
    if user.is_teacher():
        user_courses = Course.objects.filter(teacher=user)
    query = request.GET.get('query', '')
    courses = Course.objects.filter(Q(name__icontains=query) | Q(level__icontains=query) | Q(price__icontains=query))
    return render(request, "user_courses.html", {'courses': courses, 'user_courses': user_courses})

def add_course(request):
    return render(request, 'add.html')

def delete_users(request, pk):
    return render(request, 'delete_user.html')

@login_required(login_url='login')
def follow_user(request, pk):
    user = get_object_or_404(User, id=pk)
    if pk:
        user.follower.add(request.user)

        return redirect('detail', user.pk)

    return render(request, 'detail.html')
# ______________________
@login_required(login_url='login')
def unfollow_user(request, pk):
    user = get_object_or_404(User, id=pk)
    if pk:
        user.follower.remove(request.user)

        return redirect('detail', user.pk)

    return render(request, 'detail.html')

def parts(request):
    parts = Part.objects.all()
    text = _("Boshqa kurslar")
    categorys = _("Category")
    find = _("Find your course")
    search = _("Search")
    language = _("Language")
    edit = _("Edit Profile")
    set = _("Account Settings")
    help = _("Help")
    sign_out = _("Sign Out")
    light = _("Light")
    dark = _("Dark")
    auto = _("Auto")
    viewa = _("View all categories")
    title = _("Barcha kurslar")
    
    return render(request, "parts.html", {
        "parts" : parts,
        "text" : text,
        "category" : categorys,
        "find" : find,
        "search" : search,
        "language" : language,
        "edit" : edit,
        "set" : set,
        "help" : help,
        "sign_out" : sign_out,
        "light" : light,
        "dark" : dark,
        "auto" : auto,
        "viewa" : viewa,
        "title" : title,
        "parts" : parts
    })

def watch_video(request, lecture_id, video_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    video = get_object_or_404(Video, pk=video_id)

    # Update the last_watched time for the video for the current user
    video.last_watched = timezone.now()
    video.save()

    # You may also want to update the lecture's last_watched time or any other logic

    return HttpResponse("Video watched successfully!")

def last_watched_videos(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)

    last_watched_videos = lecture.videos.filter(last_watched__isnull=False).order_by('-last_watched')

    last_watched_video_ids = last_watched_videos.values_list('id', flat=True)

    return HttpResponse(f"Last watched video IDs: {', '.join(map(str, last_watched_video_ids))}")