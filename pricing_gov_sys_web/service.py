from django.conf import settings
import requests
import math
import smtplib
from email.mime.text import MIMEText


# ---------------------------------------
# CHECK USER IS LOGGED IN OR NOT
# ----------------------------------------
def is_logged_in(request):
    is_logged = request.session.get('is_logged_in', False)
    if is_logged is True:
        return True
    else:
        return False


# ---------------------------------------
# GET USER TOKEN FROM SESSION
# ----------------------------------------
def auth_token(request):
    if is_logged_in(request):
        # print("token", request.session['token'])
        return 'token ' + request.session['token']
    else:
        return None


# ---------------------------------------
# GET API RESPONSE
# ----------------------------------------
def get_api_server_response(request, params, endpoint, request_method, files=None):
    url = settings.API_SERVER + '/api/' + endpoint
    if request_method == 'get':
        return requests.get(url, params=params, headers={'Authorization': auth_token(request)})
    elif request_method == 'post':
        return requests.post(url, data=params, files=files, headers={'Authorization': auth_token(request)})
    elif request_method == 'patch':
        return requests.patch(url, data=params, headers={'Authorization': auth_token(request)})
    elif request_method == 'delete':
        return requests.delete(url, data=params, headers={'Authorization': auth_token(request)})


# ---------------------------------------
# CALCULATE TOTAL PAGE NUMBER
# ----------------------------------------
def total_page_number(total, perpage_data=settings.PERPAGE_DATA):
    return math.ceil(total / perpage_data)


# ---------------------------------------
# GENERATE PAGINATION LINK
# ----------------------------------------
def get_pagination_links(current_page, total_pages, url, keyword=None, extra_field_name=None, extra_field_value=None):
    links = ""
    if total_pages > 10:
        limit = settings.LIMIT_OF_PAGINATION_LINK
        if total_pages >= 1 and current_page <= total_pages:
            counter = 1
            links = ""
            if current_page > 1:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            current_page - 1) + ">&laquo;</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                            current_page - 1) + ">&laquo;</a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            current_page - 1) + ">&laquo;</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=' + str(
                            current_page - 1) + ">&laquo;</a></li>"

            if current_page > 2:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=1' + ">1</a></li> <li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=1' + ">1</a></li> <li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=1' + ">1</a></li> <li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=1' + ">1</a></li> <li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>"
            if current_page >= total_pages:
                cal_min_no_of_page = math.ceil(current_page - 4)
            else:
                cal_min_no_of_page = math.ceil(current_page - limit)

            if cal_min_no_of_page > 1:
                minimum_page = cal_min_no_of_page
            else:
                minimum_page = current_page

            if current_page == 1:
                cal_max_no_of_page = math.ceil(current_page + 4)
            else:
                cal_max_no_of_page = math.ceil(current_page + limit + 1)

            if cal_max_no_of_page <= total_pages:
                maximum_page = cal_max_no_of_page
            else:
                maximum_page = total_pages + 1

            for i in range(minimum_page, maximum_page):
                # if counter < limit:
                if i == current_page:
                    if keyword:
                        if extra_field_name and extra_field_value:
                            links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                        else:
                            links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                    else:
                        if extra_field_name and extra_field_value:
                            links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                        else:
                            links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?page=' + str(
                                i) + ">" + str(
                                i) + "</a></li>"
                else:
                    if keyword:
                        if extra_field_name and extra_field_value:
                            links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                        else:
                            links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                                i) + ">" + str(
                                i) + "</a></li>"
                    else:
                        if extra_field_name and extra_field_value:
                            links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                        else:
                            links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=' + str(
                                i) + ">" + str(i) + "</a></li>"
                counter = counter + 1
            if current_page < total_pages >= maximum_page:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>" + "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            total_pages) + ">" + str(
                            total_pages) + "</a></li>"
                    else:
                        links += "<li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>" + "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                            total_pages) + ">" + str(total_pages) + "</a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>" + "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            total_pages) + ">" + str(total_pages) + "</a></li>"
                    else:
                        links += "<li class=\"pagination-dot\"><a><i class=\"fa fa-ellipsis-h\" aria-hidden=\"true\"></i></a></li>" + "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=' + str(
                            total_pages) + ">" + str(total_pages) + "</a></li>"
            if 1 < total_pages != current_page:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            current_page + 1) + ">&raquo;</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                            current_page + 1) + ">&raquo;</a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            current_page + 1) + ">&raquo;</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=' + str(
                            current_page + 1) + ">&raquo;</a></li>"
    else:
        for i in range(1, total_pages + 1):
            # if counter < limit:
            if i == current_page:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            i) + ">" + str(i) + "</a></li>"
                    else:
                        links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                            i) + ">" + str(i) + "</a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            i) + ">" + str(i) + "</a></li>"
                    else:
                        links += "<li class=\"page-item active\"><a class=\"page-link\" href=" + url + '?page=' + str(
                            i) + ">" + str(i) + "</a></li>"
            else:
                if keyword:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            i) + ">" + str(i) + "</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?keyword=' + keyword + '&page=' + str(
                            i) + ">" + str(
                            i) + "</a></li>"
                else:
                    if extra_field_name and extra_field_value:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?' + extra_field_name + '=' + extra_field_value + '&page=' + str(
                            i) + ">" + str(
                            i) + "</a></li>"
                    else:
                        links += "<li class=\"page-item\"><a class=\"page-link\" href=" + url + '?page=' + str(
                            i) + ">" + str(i) + "</a></li>"
    return links


# ------------------------------------------------------
#   SEND EMAIL WITH CONTENT
# ------------------------------------------------------
def send_email(subject, email_address, email_body_content):
    # START confirmation email
    sender = 'noreply@pricing.com'
    recipient = email_address
    msg = MIMEText(email_body_content, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    server = smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
    # END confirmation email


# ------------------------------------------------------
#   CLEAR LOGIN SESSION DATA
# ------------------------------------------------------
def clear_login_session_data(request):
    request.session.modified = True

    try:
        del request.session["token"]
    except:
        pass

    try:
        del request.session["is_logged_in"]
    except:
        pass

    try:
        del request.session["user_id"]
    except:
        pass

    try:
        del request.session["username"]
    except:
        pass

    try:
        del request.session["email"]
    except:
        pass

    try:
        del request.session["image"]
    except:
        pass


# ------------------------------------------------------
#   STORE LOGIN SESSION DATA
# ------------------------------------------------------
def store_logged_user_data_in_session(request, result):
    request.session.modified = True
    request.session["token"] = result['token']
    request.session["is_logged_in"] = True
    request.session["user_id"] = result['id']
    request.session["username"] = result["name"]
    request.session["email"] = result["email"]
    request.session["image"] = "/static/logo/no-img.jpeg"


# ------------------------------------------------------
#   GET BACK LINK
# ------------------------------------------------------
def back_to(request):
    return request.META.get('HTTP_REFERER', '/')


# get_all_active_year
def get_all_active_year(request):
    active_year_response = get_api_server_response(
        request, {}, 'all-active-year', 'get')
    if active_year_response.status_code == 200:
        result = active_year_response.json()
        return result['data']
    else:
        return None


# get-draft-active-year
def get_all_year(request):
    active_year_response = get_api_server_response(
        request, {}, 'get-draft-active-year', 'get')
    if active_year_response.status_code == 200:
        result = active_year_response.json()
        return result['data']
    else:
        return None
