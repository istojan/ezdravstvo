from django.shortcuts import render

# Create your views here.


# @login_required(login_url='login:index')  # With this, if no user is logged in, than you will be redirected to the login page
def homepage(request, doctor_id):
    # print("\n\n\n We are now in doctor homepage view \n\n\n")
    return render(request, 'doctor/homepage_doctor.html',
                  {'username': request.user.get_username(),
                   'password': request.user.password, 'doc_ID': request.user.doctor.doctor_id})