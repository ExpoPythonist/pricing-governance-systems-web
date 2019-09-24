from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from pricing_gov_sys_web.service import *
from django.contrib import messages
from .service import *
import datetime
import json


# User signin
def login(request):
    now = datetime.datetime.now()
    if is_logged_in(request) is True:
        clear_login_form_data(request)
        return redirect('dashboard', year=now.year)
    else:
        if request.method == "GET":
            redirect_path = request.GET.get(
                "path", '/dashboard/' + str(now.year))
            return render(request, "user/login.html", {
                'redirect_path': redirect_path
            })

        elif request.method == "POST":
            is_login = is_permitted_to_logged_in(request)
            if is_login:
                clear_login_form_data(request)
                redirect_path = request.POST.get(
                    'redirect_path', '/dashboard/' + str(now.year))
                return JsonResponse({'redirect_path': redirect_path}, status=200)
            else:
                store_login_form_data(request)
                return JsonResponse({}, status=400)


# logout
def logout(request):
    # if is_logged_in(request) is True:
    is_logged_out = is_logged_out_user(request)
    # if is_logged_out:
    messages.add_message(request, messages.SUCCESS,
                         "You have successfully logged out.")
    return redirect('login')
    # else:
    #     messages.add_message(request, messages.ERROR, "Your login session is expired. Please login again.")
    #     return redirect('login')


# else:
#     messages.add_message(request, messages.ERROR, "Your login session is expired. Please login again.")
#     return redirect('login')


# add_new_admin
def add_new_admin(request):
    if is_logged_in(request):
        if request.method == "GET":
            page_header = "Settings"
            return render(request, "user/add-edit-user.html", {"page_header": page_header, "all_years":get_all_year(request)})
        elif request.method == "POST":
            if is_create_user(request):
                messages.add_message(
                    request, messages.SUCCESS, 'Your have successfully added new user.')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Failed to create user account')
            return redirect(back_to(request))
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')

def admin_settings(request):
    if is_logged_in(request):
        if request.method == "GET":
            page_header = "Settings"
                
            return render(request, "admin/settings.html", {"page_header": page_header, "volume": get_volume(), "all_years":get_all_year(request)})
        elif request.method == "POST":
            if update_settings(request):
                messages.add_message(
                    request, messages.SUCCESS, 'Your have successfully update the settings.')
            else:
                messages.add_message(
                    request, messages.ERROR, 'Failed to update the settings')
            return redirect(back_to(request))
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')
