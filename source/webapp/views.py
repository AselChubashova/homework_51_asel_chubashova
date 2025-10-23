from django.shortcuts import render, redirect
import random


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))

class Cat:
    IMG_HAPPY = 'webapp/cat_happy.jpg'
    IMG_NEUTRAL = 'webapp/cat_neutral.jpg'
    IMG_SAD = 'webapp/cat_sad.jpg'

    def __init__(self, name, age=1, fullness=40, happiness=40, sleeping=False):
        self.name = name
        self.age = age
        self.fullness = fullness
        self.happiness = happiness
        self.sleeping = sleeping

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'fullness': self.fullness,
            'happiness': self.happiness,
            'sleeping': self.sleeping,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def avatar(self):
        if self.happiness >= 70:
            return self.IMG_HAPPY
        elif self.happiness >= 30:
            return self.IMG_NEUTRAL
        return self.IMG_SAD

    def feed(self):
        if self.sleeping:
            return "sleeping"
        self.fullness += 15
        self.happiness += 5
        if self.fullness > 100:
            self.happiness -= 30
        self._clamp()
        return "fed"

    def play(self):
        if self.sleeping:
            self.sleeping = False
            self.happiness -= 5
        if random.randint(1, 3) == 1:
            self.happiness = 0
            self.fullness -= 10
            self._clamp()
            return "rage"
        else:
            self.happiness += 15
            self.fullness -= 10
            self._clamp()
            return "played"

    def sleep(self):
        self.sleeping = True
        self._clamp()
        return "sleeping"

    def _clamp(self):
        self.fullness = clamp(self.fullness)
        self.happiness = clamp(self.happiness)


SESSION_KEY = 'cat_state'

def _get_cat_from_session(request):
    data = request.session.get(SESSION_KEY)
    if data:
        return Cat.from_dict(data)
    return None

def _save_cat_to_session(request, cat):
    request.session[SESSION_KEY] = cat.to_dict()
    request.session.modified = True

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'Кот').strip()
        cat = Cat(name)
        _save_cat_to_session(request, cat)
        return redirect('cat_view')
    return render(request, 'webapp/index.html')

def cat_view(request):
    cat = _get_cat_from_session(request)
    if not cat:
        return redirect('index')

    message = None
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'feed':
            res = cat.feed()
            if res == 'sleeping':
                message = 'Кот спит — покормить нельзя.'
            else:
                message = 'Вы покормили кота.'
        elif action == 'play':
            res = cat.play()
            if res == 'rage':
                message = 'Кот рассержен! Счастье упало до 0.'
            else:
                message = 'Вы поиграли с котом.'
        elif action == 'sleep':
            cat.sleep()
            message = 'Кот уснул.'
        _save_cat_to_session(request, cat)

    return render(request, 'webapp/cat.html', {
        'cat': cat,
        'avatar_url': '/static/' + cat.avatar(),
        'message': message,
    })
from django.shortcuts import render

