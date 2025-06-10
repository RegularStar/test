from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import Question, Choice
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import F
from django.utils import timezone
from django.views.generic import DetailView
from django.http import Http404

# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
# 	question = get_object_or_404(Question, pk=question_id)
# 	return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )


class DetailView(DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.pub_date > timezone.now():
            raise Http404("Question not found")
        return obj


# 결과 페이지
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"


# 투표 처리 로직
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


class QuestionCreateView(generic.CreateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")


class QuestionUpdateView(generic.UpdateView):
    model = Question
    fields = ["question_text", "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")


class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")
