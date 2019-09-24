from pricing_gov_sys_web.service import *
from django.contrib import messages
from django.conf import settings
from django.core.validators import validate_email


# is_upload_new_file
def is_upload_new_file(request):
    file = request.FILES.get("file")
    year = request.POST.get("year", None)
    params = {
        "year": year
    }

    files = {'file': file}

    response = get_api_server_response(
        request, params, 'upload-file', 'post', files)
    if response.status_code == 201:
        return True
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    else:
        return False


# Get dashboard data
def get_dashboard_data(request, year):
    params = {
        "year": year,
        "number_of_top_data": 10
    }
    response = get_api_server_response(request, params, 'dashboard-data', 'get')
    if response.status_code == 200:
        result = response.json()
        return result
    elif response.status_code == 401:
        clear_login_session_data(request)
    else:
        return {}


# get pricing data
def get_pricing_data_by_year(request, year):
    page = request.GET.get('page', 1)
    params = {
        "year": year,
        "page": page
    }
    response = get_api_server_response(request, params, 'get-file-data', 'get')
    page_header = "Dashboard"
    page_title = str(year) + " Dashboard"
    if response.status_code == 200:
        result = response.json()
        total_data = int(result['total_count'])
        current_page = int(result["page"])
        total_pages = total_page_number(total_data)

        table_header = [
            "id",
            "profile_center",
            "Segmentation",
            "customer_code_ship_to",
            "customer_name_ship_to",
            "customer_code_sold_to",
            "customer_name_sold_to",
            "material_number_code",
            "material_name",
            "freight_type_code",
            "freight_types",
            "best_fit_acc_man",
            "manf_plant",
            "sold_to_region",
            "product_category",
            "product_family",
            "sales_volume_mt",
            "per_gross_sales_usd",
            "volume_price_benchmark",
            "invoice_price",
            "freight_costs",
            "freight_revenue",
            "other_discounts_and_rebates",
            "pocket_price",
            "cogs",
            "pocket_margin",
            "pocket_index",
            "rf_sales_volume_mt",
            "rf_per_gross_sales_usd",
            "ilc_volume_price_benchmark",
            "ilc_invoice_price",
            "ilc_freight_costs",
            "ilc_freight_revenue",
            "ilc_other_discounts_and_rebates",
            "ilc_pocket_price",
            "ilc_cogs",
            "ilc_pocket_margin",
            "ilc_pocket_index",
            "extracted_currency_code",
            "missing_currency_code_marked_as_usd",
            "currency_code_computation",
            "currency_code_final",
            "xchg_rate_used",
            "current_xchange_rate"
        ]

        data = {
            "page_header": page_header,
            "page_title": page_title,
            "table_header": table_header,
            "price_data": result['data'],
            "current_page": current_page,
            "total_pages": total_pages,
            "total_data": total_data,
            'start': settings.PERPAGE_DATA * current_page - settings.PERPAGE_DATA,
            "pagination_links": get_pagination_links(current_page, total_pages, "/dashboard/" + str(year))
        }
        return data
    else:
        data = {
            "page_header": page_header,
            "page_title": page_title,
            "table_header": "",
            "price_data": [],
            "current_page": 0,
            "total_pages": 0,
            "total_data": 0,
            'start': 0,
            "pagination_links": ""
        }
        return data


# get_file_upload_status
def get_file_upload_status(request):
    response = get_api_server_response(request, {}, 'get-progress', 'get')
    if response.status_code == 200:
        return response.json()
    return 0


# get data latest info
def get_latest_data_info(request, year):
    response = get_api_server_response(request, {'year': year}, 'get-year-info', 'get')
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    return False


# change_latest_year_data_status
def change_latest_year_data_status(request):
    year_id = request.POST.get('year_id', None)
    status = request.POST.get('status', None)
    if year_id and status:
        params = {
            "year_id": year_id,
            "status": status
        }
        response = get_api_server_response(request, params, 'change-data-status', 'get')
        if response.status_code == 200:
            if status == '0':
                pass
                # messages.add_message(request, messages.SUCCESS, "Your data successfully discard.")
            else:
                messages.add_message(request, messages.SUCCESS, "Your data successfully saved.")
            return response.status_code
        elif response.status_code == 401:
            messages.add_message(
                request, messages.ERROR, "Your login session is expired. Please login again.")
            clear_login_session_data(request)
            return 401
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Try again.")
            return 400
    else:
        messages.add_message(request, messages.ERROR, "Something went wrong. Try again.")
        return 400
