from django.contrib.sitemaps import Sitemap

from services import services
from post.models import Post


class PostSitemap(Sitemap):
    changefrec = 'monthly'
    priority = 0.9

    def items(self):
        return services.all_objects(Post.published)

    def lastmod(self, obj):
        return obj.updated
