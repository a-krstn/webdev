from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from .models import Post, Comment


class IsPostOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        return self.request.user.is_superuser or self.request.user == post.author


class IsCommentOwnerOrAdminMixin(UserPassesTestMixin):
    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        return self.request.user.is_superuser or self.request.user == comment.author
