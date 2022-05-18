from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import ScoreCardCreator
from .forms import ScoreCardCreatorModelForm


@login_required
def create_scorcard_view(request):
    form = ScoreCardCreatorModelForm(
        request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = ScoreCardCreatorModelForm()
    template_name = 'scorecards/form.html'
    context = {'form': form}
    return render(request, template_name, context)
