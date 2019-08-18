from django.shortcuts import render


def exercise_list(request):
    return render(request, 'tracker/exercise_list.html', {})
