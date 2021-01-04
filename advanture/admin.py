from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin

from advanture.models import Category, Advanture, Location, Images, Comment


class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_advantures_count', 'related_advantures_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Advanture,
                'category',
                'advantures_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Advanture,
                 'category',
                 'advantures_count',
                 cumulative=False)
        return qs

    def related_advantures_count(self, instance):
        return instance.advantures_count
    related_advantures_count.short_description = 'Related advantures (for this specific category)'

    def related_advantures_cumulative_count(self, instance):
        return instance.advantures_cumulative_count
    related_advantures_cumulative_count.short_description = 'Related advantures (in tree)'

admin.site.register(Category, CategoryAdmin2)

class LocationAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title',
                    'related_advantures_count', 'related_advantures_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    # inlines = [Category]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Location.objects.add_related_count(
                qs,
                Advanture,
                'location',
                'advantures_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Location.objects.add_related_count(qs,
                 Advanture,
                 'location',
                 'advantures_count',
                 cumulative=False)
        return qs

    def related_advantures_count(self, instance):
        return instance.advantures_count
    related_advantures_count.short_description = 'Related advantures (for this specific location)'

    def related_advantures_cumulative_count(self, instance):
        return instance.advantures_cumulative_count
    related_advantures_cumulative_count.short_description = 'Related advantures (in tree)'

admin.site.register(Location, LocationAdmin2)



class AdvantureImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('image_tag',)
    extra = 5


class AdvantureAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag', 'status', 'category']
    list_filter = ['status', 'category']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [AdvantureImageInline]

admin.site.register(Advanture, AdvantureAdmin)

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','advanture','image_tag']

admin.site.register(Images,ImagesAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject','comment', 'status','create_at']
    list_filter = ['status']
    readonly_fields = ('subject','comment','ip','user','advanture','rate','id')

admin.site.register(Comment,CommentAdmin)