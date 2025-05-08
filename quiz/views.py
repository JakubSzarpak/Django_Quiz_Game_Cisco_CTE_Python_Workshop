import random
from django.shortcuts import render, redirect  # type: ignore
from .models import Participant

ALL_QUESTIONS = [
    {'text': 'What is rpm?', 'options': ['suse packet manager', 'rhel packet manager', 'ubuntu packet manager', 'arch packet manager'], 'correct': 1},
    {'text': 'Which one is the type 1 hypervisor?', 'options': ['EsXi', 'VMWARE', 'Vbox', 'qemu'], 'correct': 0},
    {'text': 'What area does DPI/DPS belong to in networking?', 'options': ['Bandwidth', 'Security', 'Latency', 'L2 Switching'], 'correct': 1},
    {'text': 'What is bigger: DataLake or DataWarehouse?', 'options': ['DataLake', 'DataWarehouse', 'Equal', 'idk'], 'correct': 0},
    {'text': 'What is Redis?', 'options': ['Database', 'Framework', 'Library', 'WWW Server'], 'correct': 0},
]
MAX_QUESTIONS = 5


def quiz_view(request):
    # RESTART QUIZ
    if request.method == 'GET' and request.GET.get('redo'):
        for key in ('questions', 'current', 'score'):
            request.session.pop(key, None)
        return redirect('quiz')

    # POST HANDLER 
    if request.method == 'POST':
        # SUBMIT NAME INTO DB
        if 'name' in request.POST:
            request.session['player_name'] = request.POST['name']
            return redirect('quiz')

        # CONFIRMATION 
        if 'confirm' in request.POST:
            if request.POST['confirm'] == 'no':
                name = request.session.get('player_name', '')
                request.session.clear()
                return render(request, 'quiz/result.html', {'name': name, 'score': None, 'abort': True})

            #  AFTER CONFIRMATION --> START QUIZ
            request.session['questions'] = random.sample(
                ALL_QUESTIONS, min(MAX_QUESTIONS, len(ALL_QUESTIONS))
            )
            request.session['current'] = 0
            request.session['score'] = 0
            return redirect('quiz')

        # INDEX BASED ANSWER CHECK 
        idx = request.session.get('current', 0)
        choice = int(request.POST.get('choice', -1))
        questions = request.session['questions']
        question = questions[idx]

        if 0 <= choice < len(question['options']):
            # SCORE UPDATE
            if choice == question['correct']:
                request.session['score'] += 1
            else:
                request.session['score'] -= 1

        # +1 IN INDEX NEXT QUESTION
        request.session['current'] = idx + 1

        # IF FINISHED --> SHOW RESULT
        if request.session['current'] >= len(questions):
            Participant.objects.create(
                name=request.session['player_name'],
                score=request.session['score']
            )
            return render(request, 'quiz/result.html', {
                'name': request.session['player_name'],
                'score': request.session['score'],
                'abort': False,
            })

        return redirect('quiz')

    # DJANGO VIEWS PROCESSING
    name = request.session.get('player_name')
    if not name:
        return render(request, 'quiz/name.html')

    if 'questions' not in request.session:
        return render(request, 'quiz/greet.html', {'name': name})

    idx = request.session.get('current', 0)
    questions = request.session['questions']

    # RESULT SHOW
    if idx >= len(questions):
        return render(request, 'quiz/result.html', {
            'name': name,
            'score': request.session.get('score', 0),
            'abort': False,
        })

    # INDEX FOR CURRENT QUESTION
    question = questions[idx]
    context = {
        'num': idx + 1,
        'total': len(questions),
        'text': question['text'],
        'options': list(enumerate(question['options'])),
        'score': request.session.get('score', 0),
        'timer': 30,
    }
    return render(request, 'quiz/question.html', context)
