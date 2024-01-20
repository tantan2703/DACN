# views.py
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from .models import Comment, Post
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
def blog(request):
    context={
    }
    return render(request,'Musical/blog.html',context)

def blog_list(request):
    posts=Post.objects.all()
    paginator = Paginator(posts,6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    context={
        'posts':paged_listings,
       
    }
    return render(request, "blog/blog.html",context)

def blog_detail(request, post_title):
    post = get_object_or_404(Post, title=post_title)
    comments = Comment.objects.filter(post=post)
    comment_count = comments.count()

    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'comment_count': comment_count})

def blog_comment(request, post_title):
    post = get_object_or_404(Post, title=post_title)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request=request, data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()

            # Trả về dữ liệu JSON để cập nhật trang
            comments = Comment.objects.filter(post=post)
            comment_count = comments.count()
            response_data = {
                'status': 'success',
                'comments_html': render_to_string('blog/comment_list_partial.html', {'comments': comments, 'post': post}),
                'comment_count': comment_count,
            }
            return JsonResponse(response_data)
        else:
            # Trả về thông báo lỗi nếu form không hợp lệ
            errors = {field: ', '.join(errors) for field, errors in form.errors.items()}
            response_data = {'status': 'error', 'errors': errors}
            return JsonResponse(response_data, status=400)
    else:
        # Xử lý trường hợp yêu cầu không phải là POST hoặc người dùng không được xác thực
        # Ví dụ: bạn có thể trả về một JsonResponse trống
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def like_comment(request, post_title, comment_id):
    post = get_object_or_404(Post, title=post_title)
    comment = get_object_or_404(Comment, pk=comment_id, post=post)

    if request.user in comment.likes.all():
        # Nếu người dùng đã thích, hủy thích
        comment.likes.remove(request.user)
    else:
        # Nếu người dùng chưa thích, thêm vào danh sách thích
        comment.likes.add(request.user)

    like_count = comment.likes.count()
    return JsonResponse({'like_count': like_count, 'is_liked': request.user in comment.likes.all()})

