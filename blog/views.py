from django.shortcuts import render, reverse, redirect
from . models import Post
from django.views.generic import ListView
from django.views import View
from . forms import CommentForm 
from django.http import HttpResponseRedirect
# Create your views here.


# def startingPage(request):
#     latestPosts = Post.objects.all().order_by("-date")[:3]
#     # djang already slices when fetching the data from the database, thus not hampering the performance
#     # note: django doesn't support negative indexing here
 
#     return render(request, 'index.html', {'posts':latestPosts})
class StartingPage(ListView):
    template_name = 'index.html'
    model = Post
    ordering = ["-date", "-id"]
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


# def posts(request):
#     allPosts = Post.objects.all().order_by("date")
#     return render(request, 'all-posts.html', {'allPosts':allPosts})
class AllPostView(ListView):
    template_name = 'all-posts.html'
    model = Post
    ordering = ["-date", "-id"]
    context_object_name = 'allPosts'



# def postDetail(request, slug):
#     # allPosts = Post.objects.all()
#     # post = None
#     # for x in allPosts:
#     #     if(x['slug'] == slug):
#     #         post = x
#     # identifiedPost = post
#     try:
#         identifiedPost = Post.objects.get(slug=slug)
#     except:
#         return render(request, "404.html")


#     return render(request, 'post-detail.html', {'post':identifiedPost, 'postTags':identifiedPost.tags.all()})

class SinglePostView(View):
    def isStoredPosts(self, request, postId):
        storedPosts = request.session.get('stored_posts')
        if(storedPosts is not None):
            isSavedForLater = postId in storedPosts
        else:
            isSavedForLater = False

        return isSavedForLater

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)        

        context = {
            'post':post,
            'postTags':post.tags.all(),
            'commentForm': CommentForm(),
            'comments': post.comments.all().order_by("-id"),
            'savedForLater': self.isStoredPosts(request, post.id)
        }

        return render(request, 'post-detail.html', context)

    def post(self, request, slug):
        commentForm = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if(commentForm.is_valid()):
            comment = commentForm.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))
             
        context = {
            'post':post,
            'postTags':post.tags.all(),
            'commentForm': CommentForm(),
            'comments': post.comments.all().order_by("-id"),
            'savedForLater': self.isStoredPosts(request, post.id)
        }
        return render(request, "post-detail.html", context)


class ReadLaterView(View):
    def post(self, request):
        storedPosts = request.session.get('stored_posts')

        if(storedPosts is None):
            storedPosts = []
        postId = int(request.POST['post_id'])
        if(postId not in storedPosts):
            storedPosts.append(postId)            
        else:
            storedPosts.remove(postId)
        request.session['stored_posts'] = storedPosts
        
        return redirect('/')

    def get(self, request):
        storedPosts = request.session.get('stored_posts')
        context = {}
        isSavedForLater = True

        if(storedPosts is None or len(storedPosts)==0):
            context['posts'] = []
            context['hasPosts'] = False
        else:
            posts = Post.objects.filter(id__in = storedPosts) # only picks out the post with ids which are in storedPosts\
            context['posts'] = posts
            context['hasPosts'] = True

        return render(request, 'stored-posts.html', context)



