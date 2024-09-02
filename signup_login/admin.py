from django.contrib import admin
# from banao_task1 import signup_login
from signup_login.models import User,Category,BlogPost

# Register your models here.

class users(admin.ModelAdmin):
    list_display=['id','first_name','last_name','profile_picture','username','email','user_type','address_line1','city','state','pincode']

admin.site.register(User,users)



class category(admin.ModelAdmin):
    list_display=['name']

class blogs(admin.ModelAdmin):
    list_display=['author','title','image','category','summary','content','is_draft','created_at','updated_at']


admin.site.register(Category,category)
admin.site.register(BlogPost,blogs)
