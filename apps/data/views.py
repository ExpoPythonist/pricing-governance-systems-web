from django.shortcuts import render, redirect
from pricing_gov_sys_web.service import *
from .service import *
from django.http import JsonResponse
import datetime


# upload_file


def upload_file(request):
    if is_logged_in(request):
        if request.method == "GET":
            page_header = "Dashboard"
            year_dropdown = {}
            for y in range(2016, (datetime.datetime.now().year + 1)):
                year_dropdown.update({y: y})

            return render(request, "file-upload/file-upload.html", {
                "page_header": page_header,
                "all_years": get_all_year(request),
                'year': datetime.datetime.now().year,
                'year_drop_down': sorted(year_dropdown, reverse=True)
            })
        elif request.method == "POST":
            if is_upload_new_file(request):
                messages.add_message(
                    request, messages.SUCCESS, 'Your file successfully uploaded.')
                return render(request, "partials/messages.html", status=201)
            else:
                messages.add_message(
                    request, messages.ERROR, 'Failed to upload file.')
                return render(request, "partials/messages.html", status=500)
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        clear_login_session_data(request)
        return redirect('login')


# dashboard
def dashboard(request, year):
    if is_logged_in(request):
        year_data_info = get_latest_data_info(request, year)
        if year_data_info is False:
            return redirect('upload-file')
        else:
            response = get_dashboard_data(request, year)
            # return JsonResponse(response)
            return render(request, "dashboard/index.html", {
                'items': response,
                'year_data_info': year_data_info,
                'year': year,
                "all_years": get_all_year(request),
                "active_dashboard": int(year)
            })
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        clear_login_session_data(request)
        return redirect('login')


# upload_file_progress
def upload_file_progress(request):
    response = get_file_upload_status(request)
    return JsonResponse({"data": response}, status=200)


# change_data_status
def change_data_status(request):
    if is_logged_in(request):
        response = change_latest_year_data_status(request)

        status = request.POST.get('status', None)

        if status == "0":
            messages.add_message(request, messages.ERROR, "New data has been discarded. Would you like to upload a new file?")

        return JsonResponse({'status': response}, status=200)
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        clear_login_session_data(request)
        return JsonResponse({'status': 401}, status=200)
