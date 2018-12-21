from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Video
from .forms import VideoCreateForm
from .mixins import MemberRequiredMixin, StaffMemberRequiredMixin


# Create your views here.


class VideoList(StaffMemberRequiredMixin,ListView):
    #queryset = Video.objects.all()
    template_name = "videos/list-view.html"

    # this can be used for searching also
    # def get_queryset(self):
    #     return Video.objects.filter(title__icontains='vid') #.filter(user=self.request.user)
    def get_queryset(self):
        request = self.request
        qs = Video.objects.all()
        query = request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def list_view(request):
    qs = Video.objects.all()
    context = {
        "object_list": qs
    }
    return render(request, "videos/list-view.html", context)


class VideoDetail(MemberRequiredMixin,DetailView):
    queryset = Video.objects.all()
    # def get_object(self):
    #     abc = self.kwargs.get("abc")
    #     print(abc)
    #     return get_object_or_404(Video, slug=abc)
    template_name = "videos/detail-view.html"


def detail_view(request, pk):
    qs = Video.objects.get(pk=pk)
    context = {
        "object": qs
    }
    return render(request, "videos/detail-view.html", context)


class VideoCreate(StaffMemberRequiredMixin,CreateView):
    model = Video
    form_class = VideoCreateForm
    template_name = "videos/create-view.html"
    # success_url = "/video-list/"


def create_view(request):
    forms = VideoCreateForm(request.POST or None)
    context = {
        "form": forms
    }
    if forms.is_valid():
        obj = forms.save(commit=False)
        obj.save()
        return redirect('/video-list/')
    return render(request, "videos/create-view.html", context)


class VideoUpdate(StaffMemberRequiredMixin,UpdateView):
    queryset = Video.objects.all()
    form_class = VideoCreateForm
    template_name = "videos/update-form.html"


class VideoDelete(StaffMemberRequiredMixin,DeleteView):
    queryset = Video.objects.all()
    success_url = "/video-list/"
    template_name = "videos/delete-view.html"
