from django.db.models.query import QuerySet


class ArtistQuerySet(QuerySet):

    def listed(self):
        return self.filter(listed=True, priority__gt=0)

ArtistManager = ArtistQuerySet.as_manager


'''Example usage'''

# from .managers import PostManager
#    class Post(Postable):
#        ...
#        objects = PostManager()

# public = Post.objects.public_posts()
# public_apology = Post.objects.public_posts().filter(message_startswith="Sorry")
