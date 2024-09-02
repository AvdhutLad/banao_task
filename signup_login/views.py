from django.contrib import messages
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render,HttpResponse,HttpResponseRedirect,get_object_or_404
from signup_login import models
from signup_login.models import BlogPost, Category, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.text import Truncator



# Create your views here.
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        user_type = request.POST.get('userType')
        address_line1 = request.POST.get('addressLine1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, 'signup.html')

        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
                user_type=user_type,
                address_line1=address_line1,
                city=city,
                state=state,
                pincode=pincode
            )
            if len(request.FILES)!=0:
                user.profile_picture=request.FILES['profilePicture']
            user.save()
            messages.success(request, "Signup successful! You can now log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "An error occurred while processing your request. Please try again.")
        except ValidationError as e:
            messages.error(request, str(e))
    
    return render(request, 'Signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['user_type'] = user.user_type

            if user.user_type == 'doctor':
                return HttpResponseRedirect(f'/doctor_dashboard/?user_id={user.id}')
            elif user.user_type == 'patient':
                return HttpResponseRedirect(f'/patient_dashboard/?user_id={user.id}')
        except User.DoesNotExist:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')


def doctor_dashboard(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return HttpResponseBadRequest("User ID is missing.")
    
    try:
        user = User.objects.get(id=user_id)
        context = {
            'user': user,
         
        }
        return render(request, 'doctor_dashboard.html', context)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found.")


def truncate_summary(summary, word_limit=15):
    truncated_summary = Truncator(summary).words(word_limit, truncate=' ...')
    return truncated_summary

def patient_dashboard(request):
    
    user_id = request.GET.get('user_id')
    category_id = request.GET.get('category_id')
    page_number = request.GET.get('page', 1)
    
    if not user_id:
        return HttpResponseBadRequest("User ID is missing.")
    
    try:
        user = User.objects.get(id=user_id)
        categories = Category.objects.all()
        
        if category_id:
            blogs = BlogPost.objects.filter(category_id=category_id, is_draft=False)
        else:
            blogs = BlogPost.objects.filter(is_draft=False)
        
        # Truncate summaries
        for blog in blogs:
            blog.summary = truncate_summary(blog.summary)
        
        paginator = Paginator(blogs, 5)
        paginated_blogs = paginator.get_page(page_number)
        
        context = {
            'user': user,
            'categories': categories,
            'blogs': paginated_blogs,
            'selected_category': category_id,
        }
        return render(request, 'patient_dashboard.html', context)
    except User.DoesNotExist:
        return HttpResponseBadRequest("User not found.")
    
def logout(request):
    request.session.flush()
    return redirect('login')



def addBlog(request):
    cate = Category.objects.all()
    user_id = request.session.get('user_id')  # Get the user ID from the session
    if not user_id:
        messages.error(request, 'You must be logged in to add a blog post.')
        return redirect('login')  # Redirect to your login page

    user = User.objects.get(pk=user_id) 

    if request.method == "POST":
        # Create a new BlogPost object
        blog = BlogPost()
        blog.title = request.POST.get('title')
        print(blog.title)
        category_id = request.POST.get('category')
        print(category_id)
        try:
            blog.category = Category.objects.get(pk=category_id)
            print("working1")
        except Category.DoesNotExist:
            print("working2")
            messages.error(request, 'Selected category does not exist.')
            return render(request, 'addBlog.html', {'categories': cate, 'form': request.POST})

        blog.summary = request.POST.get('summary')
        blog.content = request.POST.get('content')
        blog.is_draft = request.POST.get('is_draft') == 'on'
        print(user)
        blog.author = user
        print("working3")
        if len(request.FILES) != 0:
            blog.image = request.FILES['image']

        try:

            blog.save()
            if blog.is_draft:
                messages.success(request, 'Blog post saved as draft successfully.')
            else:
                messages.success(request, 'Blog post published successfully.')
        except Exception as e:
            messages.error(request, f'There was an error saving the blog post: {e}')

        return render(request, 'addBlog.html', {'categories': cate})

    return render(request, 'addBlog.html', {'categories': cate})


def manageBlog(request):
    user_id = request.session.get('user_id') 
    if not user_id:
        messages.error(request, 'You must be logged in to add a blog post.')
        return redirect('login')  

    user = User.objects.get(pk=user_id) 
    published_blogs = BlogPost.objects.filter(author=user, is_draft=False)
    draft_blogs = BlogPost.objects.filter(author=user, is_draft=True)

    context = {
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs
    }
    return render(request,'manageBlog.html',context)



def deleteBlog(request, blog_id):
    user_id = request.session.get('user_id') 
    if not user_id:
        messages.error(request, 'You must be logged in to add a blog post.')
        return redirect('login')  

    user = User.objects.get(pk=user_id)
    blog = get_object_or_404(BlogPost, id=blog_id, author=user)
    blog.delete()
    messages.success(request, 'Blog post deleted successfully.')
    return redirect('manageBlog')


def editBlog(request, blog_id):
    user_id = request.session.get('user_id') 
    if not user_id:
        messages.error(request, 'You must be logged in to add a blog post.')
        return redirect('login')  

    user = User.objects.get(pk=user_id)
    
    blog = get_object_or_404(BlogPost, id=blog_id, author=user)
    categories = Category.objects.all()

    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.category_id = request.POST.get('category')
        blog.summary = request.POST.get('summary')
        blog.content = request.POST.get('content')
        blog.is_draft = request.POST.get('is_draft') == 'on'

        if 'image' in request.FILES:
            blog.image = request.FILES['image']

        try:
            blog.save()
            messages.success(request, 'Blog post updated successfully.')
            return redirect('manageBlog')
        except Exception as e:
            messages.error(request, f'There was an error updating the blog post: {e}')

    context = {
        'blog': blog,
        'categories': categories
    }
    return render(request, 'editBlog.html', context)
