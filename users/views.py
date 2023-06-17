
from django.views.generic import UpdateView

from users.forms import UserForm
from users.models import User


class ProfileUpdateView(UpdateView):
    model = User
    form_class = UserForm

    def get_object(self, queryset=None):
        return self.request.user