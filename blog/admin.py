from django.contrib import admin
from django.utils import timezone
from .models import Category, Tag, BloggerProfile, Post, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(BloggerProfile)
class BloggerProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username', 'user__email')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class PostStatusFilter(admin.SimpleListFilter):
    title = 'status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('published', 'Published'),
            ('draft', 'Draft'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'published':
            return queryset.exclude(published_date=None)
        if self.value() == 'draft':
            return queryset.filter(published_date=None)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'category', 'get_tags', 'comment_count', 'status')
    list_filter = (PostStatusFilter, 'published_date', 'category', 'tags')
    search_fields = ('title', 'content', 'author__username', 'category__name', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    inlines = [CommentInline]
    actions = ['make_published', 'make_draft']
    list_per_page = 20
    save_on_top = True
    readonly_fields = ('created_date',)
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'content')
        }),
        ('Categories and Tags', {
            'fields': ('category', 'tags'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_date', 'published_date'),
            'description': 'Set published_date to make the post public'
        })
    )

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'

    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

    def status(self, obj):
        return "Published" if obj.published_date else "Draft"
    status.short_description = 'Status'

    def make_published(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(published_date=timezone.now())
        self.message_user(request, f'{updated} posts marked as published.')
    make_published.short_description = "Mark selected posts as published"

    def make_draft(self, request, queryset):
        updated = queryset.update(published_date=None)
        self.message_user(request, f'{updated} posts marked as drafts.')
    make_draft.short_description = "Mark selected posts as drafts"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_comment', 'post', 'author', 'created_date')
    list_filter = ('created_date', 'author')
    search_fields = ('text', 'author__username')

    def truncated_comment(self, obj):
        return obj.text[:75] + '...' if len(obj.text) > 75 else obj.text
    truncated_comment.short_description = 'Comment'
