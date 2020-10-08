from .models import Debt
from src.apps.users.models import User
from django.db.models import Q


class DebtData:

    def __init__(self, debt: Debt, is_positive: bool):
        self.text = debt.text
        self.price = debt.price
        self.is_positive = is_positive
        self.created_at = debt.created_at


class UserDebtsData:

    def __init__(self, user: User):
        self.summary = 0
        self.is_positive = True
        self.debts = []
        self.user = user

    def add_debt(self, debt: Debt):
        is_positive = True
        if debt.to_user == self.user:
            is_positive = False
        self.debts.append(DebtData(debt, is_positive))
        if is_positive:
            self.summary += debt.price
        else:
            self.summary -= debt.price
        if self.summary < 0:
            self.is_positive = False


class SummaryDebtData:
    def __init__(self):
        self.summary = 0
        self.debts_count = 0
        self.users = []


def get_user_debts_data(user: User) -> SummaryDebtData:
    """
    Получить сводные данные о долгах пользователя
    :param user:
    :return:
    """
    result = SummaryDebtData()
    debts = Debt.objects.filter_by_user(user)
    if len(debts) == 0:
        return result
    unique_users = []
    for debt in debts:
        if debt.user not in unique_users:
            unique_users.append(debt.user)
        if debt.to_user not in unique_users:
            unique_users.append(debt.to_user)
    unique_users.remove(user)
    for unique_user in unique_users:
        user_debt_data = UserDebtsData(user)
        user_debts = debts.filter(Q(user=unique_user) | Q(to_user=unique_user))
        for debt in user_debts:
            user_debt_data.add_debt(debt)
        result.users.append(user_debt_data)
    for user_debt_data in result.users:
        result.summary += user_debt_data.summary
        result.debts_count += len(user_debt_data.debts)
        user_debt_data.summary = abs(user_debt_data.summary)
    return result
