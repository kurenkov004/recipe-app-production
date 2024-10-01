from django.shortcuts import render, redirect # type: ignore
# Django authentication libraries
from django.contrib.auth import authenticate, login, logout # type: ignore
# Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm # type: ignore


def login_view(request):
    # initialize error_message object to "None"
    error_message = None
    # initialize form object with username and password fields
    form = AuthenticationForm()

    # when "login" button is clicked, POST request is generated
    if request.method == "POST":
        # read the data sent by the form
        form = AuthenticationForm(data=request.POST)

        # check if form is valid
        if form.is_valid():
            # read username & password
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # use Django function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:
                # if user is authenticated, then use Django function to login
                login(request, user)
                return redirect("recipes:list")
        else:
            error_message = "something went wrong, please check your credentials"

    # prepare data to send from view to template
    context = {
        "form": form,
        "error_message": error_message,
    }
    # load the login page using "context" information that was just sent
    return render(request, "auth/login.html", context)


# logout FBV that takes request from user and re-directs back to login form
def logout_view(request):
    # use Django function
    logout(request)
    # navigate to login page
    return render(request, "auth/success.html")
