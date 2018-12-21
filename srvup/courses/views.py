from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.base import View

from .models import Course, Lecture, MyCourses
from videos.mixins import MemberRequiredMixin, StaffMemberRequiredMixin
from .forms import CourseForm
from analytics.models import CourseViewEvent


# Create your views here.


class CourseList(StaffMemberRequiredMixin, ListView):
    # queryset = Video.objects.all()
    template_name = "courses/list-view.html"

    # this can be used for searching also
    # def get_queryset(self):
    #     return Video.objects.filter(title__icontains='vid') #.filter(user=self.request.user)
    def get_queryset(self):
        request = self.request
        qs = Course.objects.all()
        query = request.GET.get('q')
        user = self.request.user
        if query:
            qs = qs.filter(title__icontains=query)
        if user.is_authenticated:
            qs = qs.owned(user)
            # qs = qs.prefetch_related(
            #     Prefetch('owned',
            #              queryset=MyCourses.objects.filter(user=user),
            #              to_attr='is_owner'
            #              )
            # )
            print(qs)
        return qs  # .filter(title__icontains='vid') #.filter(user=self.request.user)

    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super(CourseList, self).get_context_data(*args, **kwargs)
        print(dir(context.get('page_obj')))
        return context


class LectureDetailView(View):
    template_name = "courses/lecture-detail.html"

    def get(self, request, cslug=None, lslug=None, *args, **kwargs):
        obj = None
        qs = Course.objects.filter(slug=cslug).lectures().owned(request.user)
        if not qs.exists():
            raise Http404
        course_ = qs.first()
        if request.user.is_authenticated:
            view_event, created = CourseViewEvent.objects.get_or_create(user=request.user, course=course_)
            if view_event:
                view_event.views += 1
                view_event.save()
        lectures_qs = course_.lecture_set.filter(slug=lslug)
        if not lectures_qs.exists():
            raise Http404

        obj = lectures_qs.first()
        context = {
            "object": obj,
            "course": course_,
        }

        if not course_.is_owner and not obj.free:  # and not user.is_member:
            return render(request, "courses/must_purchase.html", {"object": course_})

        return render(request, "courses/lecture-detail.html", context)
    # def get_object(self):
    #     course_slug = self.kwargs.get("cslug")
    #     lecture_slug = self.kwargs.get('lslug')
    #     obj = get_object_or_404(Lecture, course__slug=course_slug, slug=lecture_slug)
    #     return obj


def lecturedetailview(request, cslug, lslug):
    context = {
        "object": Lecture.objects.get(course__slug=cslug, slug=lslug)
    }
    return render(request, "courses/lecture-detail.html", context)


def list_view(request):
    qs = Course.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "courses/list-view.html", context)


class CourseDetail(DetailView):
    # queryset = Course.objects.all()
    def get_object(self):
        slug = self.kwargs.get("slug")
        qs = Course.objects.filter(slug=slug).lectures().owned(self.request.user)
        if qs.exists():
            obj = qs.first()
            if self.request.user.is_authenticated:
                view_event, created = CourseViewEvent.objects.get_or_create(user=self.request.user, course=obj)
                if view_event:
                    view_event.views += 1
                    view_event.save()
            return obj
        raise Http404

    template_name = "courses/detail-view.html"


def detail_view(request, pk):
    qs = Course.objects.get(pk=pk)
    context = {
        "object": qs
    }
    return render(request, "courses/detail-view.html", context)


class CoursePurchaseView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self, slug=None):
        qs = Course.objects.filter(slug=slug).owned(self.request.user)
        if qs.exists():
            user = self.request.user
            if user.is_authenticated:
                my_courses = user.mycourses
                # run transaction
                # if transaction successful:
                my_courses.courses.add(qs.first())
                return qs.first().get_absolute_url()
            return qs.first().get_absolute_url()
        return "/course-list/"


class CourseCreate(StaffMemberRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/create-view.html"
    success_url = "/course-list/"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(CourseCreate, self).form_valid(form)


# def create_view(request):
#     forms = VideoCreateForm(request.POST or None)
#     context = {
#         "form": forms
#     }
#     if forms.is_valid():
#         obj = forms.save(commit=False)
#         obj.save()
#         return redirect('/video-list/')
#     return render(request, "videos/create-view.html", context)
#

class CourseUpdate(StaffMemberRequiredMixin, UpdateView):
    queryset = Course.objects.all()
    form_class = CourseForm
    template_name = "courses/update-form.html"

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super(CourseUpdate, self).form_valid(form)

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404


class CourseDelete(StaffMemberRequiredMixin, DeleteView):
    queryset = Course.objects.all()
    success_url = "/course-list/"
    template_name = "courses/delete-view.html"

    def get_object(self):
        slug = self.kwargs.get("slug")
        obj = Course.objects.filter(slug=slug)
        if obj.exists():
            return obj.first()
        raise Http404
