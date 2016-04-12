from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Question
from django.shortcuts import get_object_or_404, render

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
            'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # pk is the primary key
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
       # redisplay the question voting form
       return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # need to return with a HttpResponse() after dealing with a POSt data
        # this prevents the data from being sent twice by pressing the button 
        # two times
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

