from pricing_gov_sys_web.service import *
from django.contrib import messages
from django.conf import settings
from django.core.validators import validate_email
from user.models import Settings


# ---------------------------------------
# CHECK USER LOGIN VALIDATE OR NOT
# ----------------------------------------
def is_permitted_to_logged_in(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    error = 0
    if not request.is_ajax():
        if username and username.strip() == '':
            messages.add_message(request, messages.ERROR, "Username can't blank.")
            error += 1

        if password and password.strip() == '':
            messages.add_message(request, messages.ERROR, "Password can't blank.")
            error += 1
    else:
        if username and username.strip() == '':
            error += 1

        if password and password.strip() == '':
            error += 1

    if error > 0:
        return False
    params = {
        'username': username,
        'password': password
    }

    response = get_api_server_response(request, params, "signin", 'post')
    if response.status_code == 200:
        result = response.json()
        store_logged_user_data_in_session(request, result)
        messages.add_message(request, messages.SUCCESS, "You have successfully logged in.")
        return True
    else:
        if not request.is_ajax():
            messages.add_message(request, messages.ERROR, "Incorrect username or password. Please try again.")
        return False


# is_logged_out_user
def is_logged_out_user(request):
    clear_login_session_data(request)
    clear_login_form_data(request)
    return True
    response = get_api_server_response(request, {}, "signout", 'post')
    if response.status_code == 200:
        clear_login_session_data(request)
        clear_login_form_data(request)
        return True
    else:
        clear_login_session_data(request)
        clear_login_form_data(request)
        return True


# ---------------------------------------
# STORE LOGIN FORM DATA in SESSION
# ----------------------------------------
def store_login_form_data(request):
    username = request.POST.get('username', None)
    request.session.modified = True
    request.session["login_username"] = username


# ---------------------------------------
# DELETE LOGIN FORM  SESSION DATA
# ----------------------------------------
def clear_login_form_data(request):
    try:
        request.session.modified = True
        del request.session["login_username"]
    except:
        pass


# Registration form validation check
def is_registration_form_valid(request):
    # request.session.modified = True
    # request.session["signup_data"] = request.POST
    user_name = request.POST.get('username', None)
    user_email = request.POST.get('email', None)
    user_password = request.POST.get('password', None)
    user_confirm_password = request.POST.get('confirm_password', None)
    user_type = request.POST.get('user_type', None)
    # user_img = request.POST.get("base64_user_img", None)
    error = 0
    if not user_name.strip():
        messages.add_message(request, messages.ERROR, 'Username is required.')
        error += 1
    if not user_email.strip():
        messages.add_message(request, messages.ERROR, 'Email address is required.')
        error += 1
    elif validate_email(user_email.strip()):
        messages.add_message(request, messages.ERROR, 'Invalid email address.')
        error += 1
    if not user_password.strip():
        messages.add_message(request, messages.ERROR, 'Password is required.')
        error += 1
    elif len(user_password.strip()) < 6 or len(user_password.strip()) > 12:
        messages.add_message(request, messages.ERROR, 'Password length must be between 6 to 12 characters.')
        error += 1
    elif not user_confirm_password.strip():
        messages.add_message(request, messages.ERROR, 'Confirm password is required.')
        error += 1
    elif user_password.strip() != user_confirm_password.strip():
        messages.add_message(request, messages.ERROR, "Confirm password doesn't not match with password.")
        error += 1
    elif not user_type:
        messages.add_message(request, messages.ERROR, "User type is required.")
        error += 1
    # elif not user_img:
    #     messages.add_message(request, messages.ERROR, "User image is required.")
    #     error += 1

    if error > 0:
        return False
    else:
        return True


# is_create_user
def is_create_user(request):
    if is_registration_form_valid(request):
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')
        user_confirm_password = request.POST.get('confirm_password')
        user_img = request.POST.get("base64_user_img", None)
        user_type = request.POST.get('user_type', None)
        params = {
            'username': user_name.strip(),
            'email': user_email.strip(),
            'password': user_password.strip(),
            'confirm_password': user_confirm_password,
            'type': user_type,
            'image': None
        }
        if user_img != '':
            params.update({'image': user_img})
        response = get_api_server_response(request, params, 'new-user', 'post')

        result = response.json()
        if response.status_code == 409 or response.status_code == 400:
            non_field_errors = result.get('non_field_errors', None)
            if non_field_errors:
                messages.add_message(request, messages.ERROR, non_field_errors[0])
            user_errors = result.get('user', None)
            if user_errors:
                for error_field in user_errors:
                    messages.add_message(request, messages.ERROR, user_errors[error_field][0])
            return False
        elif response.status_code == 201:
            return True
        elif response.status_code == 401:
            return False
    else:
        return False

def update_settings(request):
    try:
        # check is any row in settings
        settings = Settings.objects.filter()

        if settings.count() == 1:
            # update
            Settings.objects.update(volume = request.POST.get('volume'))
        else:
            # insert
            Settings.objects.create(volume = request.POST.get('volume'))

        return True
    except:
        return False

def get_volume():
    settings = Settings.objects.filter()
    if settings.count() == 1:
        settings = settings.first()
        return settings.volume
    else:
        return "MT"
