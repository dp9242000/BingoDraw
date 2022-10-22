from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.utils import timezone
from django.contrib.auth import mixins
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User

from bootstrap_datepicker_plus.widgets import DateTimePickerInput

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5

    def get_queryset(self):
        """Return the questions previously posted (no future dates) and order by date desc."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class UserPollListView(generic.ListView):
    model = Question
    template_name = 'polls/user_polls.html'
    context_object_name = 'user_polls_list'
    paginate_by = 5

    def get_queryset(self):
        """Return the last five published questions."""
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Question.objects.filter(
            pub_date__lte=timezone.now(), author=user
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# Formset to be included in QuestionCreateView
ChoiceFormset = inlineformset_factory(
    Question, Choice, fields=('choice_text',), extra=2
)

class QuestionCreateView(mixins.LoginRequiredMixin, generic.CreateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ['question_text', 'pub_date']

    def get_form(self):
        """Add date picker to the form"""
        form = super(QuestionCreateView, self).get_form()
        form.fields['pub_date'].widget = DateTimePickerInput()
        return form

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.author = self.request.user
        choices = context["choices"]
        self.object = form.save()
        if choices.is_valid():
            choices.instance = self.object
            choices.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # overwrite context data to include ChoiceFormset
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["choices"] = ChoiceFormset(self.request.POST)
        else:
            data["choices"] = ChoiceFormset()
        return data

    def get_success_url(self):
        return reverse('polls:index')


class QuestionUpdateView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.UpdateView):
    model = Question
    template_name = 'polls/question_form.html'
    fields = ['question_text', 'pub_date']


    def get_form(self):
        """Add date picker to the form"""
        form = super(QuestionUpdateView, self).get_form()
        form.fields['pub_date'].widget = BSDateTimePicker()
        return form

    def form_valid(self, form):
        context = self.get_context_data()
        choices = context["choices"]
        self.object = form.save()
        if choices.is_valid():
            choices.instance = self.object
            choices.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        # overwrite context data to include ChoiceFormset
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["choices"] = ChoiceFormset(self.request.POST, instance=self.object)
        else:
            data["choices"] = ChoiceFormset(instance=self.object)
        return data

    def get_success_url(self):
        return reverse('polls:index')

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False


class QuestionDeleteView(mixins.LoginRequiredMixin, mixins.UserPassesTestMixin, generic.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'

    def test_func(self):
        question = self.get_object()
        if self.request.user == question.author:
            return True
        return False

    def get_success_url(self):
        return reverse('polls:index')


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
