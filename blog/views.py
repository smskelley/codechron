from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, render, get_list_or_404
from django.views.generic import View
from django.utils.datastructures import SortedDict
from blog.models import Author, Post, Comment

class BlogAjaxComments(View):
    template = 'ajax_comments.html'

    def get(self, request, PostId):
        comments = Comment.objects.filter(post=PostId).order_by('-pub_date')
        return render( request, self.template, { 
                       "comments": comments,
                       "PostId": PostId,
                       "ErrorMessage": "",
                     })

    def post(self, request, PostId):
        comments = Comment.objects.filter(post=PostId).order_by('-pub_date')
        errorMessage = ""

        if "name" in request.POST and len(request.POST["name"]) is 0:
            errorMessage = "Fill in name"
        if "comment" in request.POST and len(request.POST["comment"]) is 0:
            errorMessage += "Fill in comment" if len(errorMessage) is 0 else " and comment"
        elif len(errorMessage) is 0:
            comment = Comment(body = request.POST["comment"], author = request.POST["name"],
                              post = get_object_or_404(Post, id=PostId, published=True),
                              pub_date = datetime.now() )
            comment.save()
            errorMessage = "Submitted"
        errorMessage += "."

        return render( request, self.template, {
                       "comments" : comments,
                       "PostId" : PostId,
                       "ErrorMessage": errorMessage,
                     })
        
        

class BlogBase:
    AllPosts = Post.objects.filter(published=True).order_by('-pub_date')
    LatestPost = AllPosts[0]
    def BuildArchive(self):
        ''' This was useful, but then it was replaced with simple template magic '''
        Archive = SortedDict()
        years = self.AllPosts.dates('pub_date', 'year', order='DESC')
        for year in years:
            Archive[year.year] = SortedDict()
            months = self.AllPosts.filter(pub_date__year = year.year).dates('pub_date', 'month')
            for month in months:
                Archive[year.year][month.strftime("%B")] = self.AllPosts.filter(
                                                    pub_date__year = year.year,
                                                    pub_date__month = month.month,
                                                  ).order_by('-pub_date')
        return Archive

    def BuildContext(self, **kwargs):
        kwargs['AllPosts'] = self.AllPosts
        return kwargs

class BlogHome(View, BlogBase):
    def get(self, request):
        return render_to_response('index.html', BlogBase.BuildContext(self,
                                   Post = BlogBase.LatestPost))

class BlogAbout(View, BlogBase):
    def get(self, request):
        return render_to_response('about.html', BlogBase.BuildContext(self))

class BlogViewPost(View, BlogBase):
    def get(self, request, PostId = 1):
        post = get_object_or_404(Post, id=PostId, published=True)
        return render_to_response('index.html', BlogBase.BuildContext(self, Post = post))


class BlogArchive(View, BlogBase):
    def get(self, request):
        return render_to_response('archive.html', BlogBase.BuildContext(self))
