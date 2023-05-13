from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            User.objects.create_user(username=username, password=password, email=email)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('account_details')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def account_details(request):
    user_accounts = Account.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'account_details.html', {'accounts': user_accounts, 'transactions': transactions})


@login_required
def perform_withdraw(request):
    if request.method == 'POST':
        form = WithdrawForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            amount = form.cleaned_data['amount']
            account = Account.objects.get(account_number=account_number, user=request.user)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(user=request.user, account=account, transaction_type='withdraw', mode='debit', amount=amount, balance=account.balance)
                return redirect('account_details')
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = WithdrawForm()
    return render(request, 'withdraw.html', {'form': form})


@login_required
def perform_deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            amount = form.cleaned_data['amount']
            account = Account.objects.get(account_number=account_number, user=request.user)
            account.balance += amount
            account.save()
            Transaction.objects.create(user=request.user, account=account, transaction_type='deposit', mode='credit', amount=amount, balance=account.balance)
            return redirect('account_details')
    else:
        form = DepositForm()
    return render(request, 'deposit.html', {'form': form})


@login_required
def perform_transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            from_account_number = form.cleaned_data['from_account_number']
            to_account_number = form.cleaned_data['to_account_number']
            amount = form.cleaned_data['amount']
            from_account = Account.objects.get(account_number=from_account_number, user=request.user)
            to_account = Account.objects.get(account_number=to_account_number)
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                from_account.save()
                to_account.save()
                Transaction.objects.create(user=request.user, account=from_account, transaction_type='transfer', mode='debit', amount=amount, balance=from_account.balance)
                Transaction.objects.create(user=to_account.user, account=to_account, mode='credit', amount=amount, balance=to_account.balance)
                return redirect('account_details')
            else:
                form.add_error('amount', 'Insufficient funds')
    else:
        form = TransferForm()
    return render(request, 'transfer.html', {'form': form})
