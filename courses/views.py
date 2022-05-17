from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
from .models import HoleCreater
from .forms import HoleCreateModelForm


@login_required
def create_hole_view(request):
    form = HoleCreateModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = HoleCreateModelForm()
    template_name = 'courses/form.html'
    context = {'form': form}
    return render(request, template_name, context)
