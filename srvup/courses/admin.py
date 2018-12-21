from django.contrib import admin

# Register your models here.
from courses.forms import LectureAdminForm
from .models import Course, Lecture,MyCourses

admin.site.register(MyCourses)

class LectureInline(admin.TabularInline):
    model = Lecture
    prepopulated_fields = {"slug": ("title",)}
    form = LectureAdminForm
    raw_id_fields = ['video',]
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_filter = ['updated', 'timestamp']
    list_display = ['title', 'updated', 'timestamp', 'order']
    readonly_fields = ['updated', 'timestamp', 'short_title']
    search_fields = ['title', 'description']
    list_editable = [ 'order']

    class Meta:
        model = Course

    def short_title(self, obj):
        return obj.title[:3]


admin.site.register(Course, CourseAdmin)
