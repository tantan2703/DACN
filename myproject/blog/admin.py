# myapp/admin.py
from django.contrib import admin
from .models import Post, Comment

class CommentInline(admin.TabularInline):  # Hoặc sử dụng admin.StackedInline cho giao diện dạng stacked
    model = Comment
    extra = 1  # Số lượng form trống hiển thị để thêm mới comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CommentInline]  # Thêm CommentInline vào PostAdmin
