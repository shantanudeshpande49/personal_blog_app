from django.contrib import admin
from .models import Post, Tag, Author, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date")
    list_display = ("title", "date", "author")
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Author)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("userName", "post")
admin.site.register(Comment, CommentAdmin)


# to edit our data of the models we register them in the admin, 