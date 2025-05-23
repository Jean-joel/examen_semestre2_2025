from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView
from django.shortcuts import render, redirect  # Corrige 'render' et 'redirect'
from django.contrib.auth.decorators import login_required
from .models import Car  # Corrige 'Car' - import depuis vos modèles

# Vue fonction sécurisée
@login_required
@csrf_protect
def dashboard(request):
    user = request.user
    try:
        car = user.car  # Relation OneToOne
        washer = car.assigned_washer
        context = {
            'user': user,
            'car': car,
            'washer': washer
        }
        return render(request, 'users/dashboard.html', context)
    except AttributeError:
        return redirect('no_car_alert')


# Vue classe sécurisée
class CarDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Car
    template_name = 'users/car_detail.html'

    def test_func(self):
        car = self.get_object()
        return car.owner == self.request.user

    def handle_no_permission(self):
        return redirect('permission_denied')


from django.shortcuts import render

# Create your views here.
