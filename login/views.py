from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
# from .forms import UserLoginForm
from django.views.generic import View
from django.contrib.auth.decorators import login_required

from .forms import UserForm

# Create your views here.


# class UserFormView(View):
#     form_class = UserForm
#     template_name = 'login/index.html'
#
#     # display a blank form
#     def get(self, request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     # process form data
#     def post(self, request):
#         form = self.form_class(request.POST)
#
#         print("I am going to post a method")
#
#         if form.is_valid():
#
#             print("The form is valid")
#
#             user = form.save(commit=False)
#
#             # cleaned (normalized) data
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#
#             # user.set_password(password)
#
#             # method to change passord
#             user.set_password(password)
#
#             # save to database
#             # user.save()
#
#             print("Username: ", user.username)
#             print(" Password: ", user.password)
#             # print(" Email: ", user.email)
#
#
#             # returns User objects if credentials are correct
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#
#                 if user.is_active:
#                     # to log in a user
#                     login(request, user)
#                     return redirect('login:homepage', {'username', request.user.get_username()}) # redirect to home page
#             # return HttpResponse("Good Job. It worked")
#
#         return render(request, self.template_name, {'form': form})

class UserFormView(View):
    form_class = UserForm
    template_name = 'login/index.html'

    # display a blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        # form = self.form_class(request.POST)
        #
        # print("This is the form:")
        print(username)
        print(password)

        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']

        # # cleaned (normalized) data
        # username = request.cleaned_data['username']
        # password = request.cleaned_data['password']

        # returns User objects if credentials are correct
        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User is authenticated")
            if user.is_active:
                print("User is active")
                # to log in a user
                login(request, user)
                print("User is logged in atm")
                # , {'username', request.user.get_username()}
                return redirect('login:homepage')  # redirect to home page

        return render(request, self.template_name, {'form': UserForm(None)})


@login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def homepage(request):
    print("Trying to return homepage to user")

    if request.user.is_authenticated():
        print("User has been already authenticated")
        # print(request.user.get_username())
        # print(request.user.email)
        return render(request, 'login/homepage.html', {'username': request.user.get_username(), 'email': request.user.email, 'password': request.user.password})
    else:
        print("User has not been authenticated")
        return HttpResponseRedirect(reverse('login:index')) # request to default page if no user is logged in
        # return HttpResponseRedirect(UserFormView.get(UserFormView, request))
        # return render(request, 'login/index.html')

    # return HttpResponse("Hello Friend")


def logout_view(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return HttpResponseRedirect(reverse('login:index'))


# def logout_view(request):
#     logout(request)
#
#     return HttpResponseRedirect(reverse('login:index'))

# def login_view(request):
#     form = UserLoginForm(request.POST or None)
#
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#
#
#
#     return render(request, "form.html", {"form":form })


# def register_view(request):
#     return render(request, "form.html", {})
#
#
# def logout_view(request):
#     return render(request, "form.html", {})