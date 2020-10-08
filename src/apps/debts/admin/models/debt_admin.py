from src.apps.core.admin import BaseModelAdmin
from src.apps.debts.models import Debt
from django import forms


class DebtChangeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DebtChangeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Debt
        fields = ['text', 'price', 'user', 'to_user']

    def save(self, *args, **kwargs):
        debt = super(DebtChangeForm, self).save(*args, **kwargs)
        if not debt.to_user:
            debt.to_user = self.current_user
        debt.save()
        return debt


class DebtAdmin(BaseModelAdmin):
    list_display = ('to_user', 'user', 'price', 'text', 'created_at')
    form = DebtChangeForm
    add_form = DebtChangeForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super(DebtAdmin, self).get_form(request, obj, change, **kwargs)
        return form

    def get_queryset(self, request):
        user = request.user
        debts = Debt.objects.all()
        if not user.is_superuser:
            debts = debts.objects.filter_by_user(user)
        return debts
