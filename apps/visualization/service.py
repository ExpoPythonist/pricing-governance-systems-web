from pricing_gov_sys_web.service import *
from django.contrib import messages
from django.conf import settings
import datetime


# get scatter-plot chart data
def get_scatter_plot_chart_data_by_year(request):
    endpoint = 'get-scatterplot-data'
    year = request.GET.get('year', None)
    product = request.GET.get('product', None)
    customer = request.GET.get('customer', None)
    page_header = "Visualization & Analytics"
    params = {
        'year': year
    }
    if product:
        params.update({'product_family': product})
        active_page = "product-scatter"

    if customer:
        params.update({'customer': customer})
        active_page = "customer-scatter"

    response = get_api_server_response(
        request, params, endpoint, 'get')
    if response.status_code == 200:
        result = response.json()
        return {
            # "page_header": page_header,
            # "active_page": active_page,
            "all_years": get_all_year(request),
            "items": result,
            "product": product,
            "customer": customer,
            "year": year
        }
    return {
        # "page_header": page_header,
        # "active_page": active_page,
        "all_years": get_all_year(request),
        "items": [],
        "product": "",
        "year": year
    }


# Get Product list by year
def get_product_by_year(request):
    endpoint = 'get-unique-product'
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    product = request.GET.get('product', None)
    keyword = request.GET.get('keyword', product)
    page = request.GET.get('page', 1)
    limit = -1
    prams = {'year': year, 'limit': limit, 'page': page}
    if keyword:
        prams.update({"keyword": keyword})

    response = get_api_server_response(request, prams, endpoint, 'get')

    # all_products_response = get_api_server_response(request, {'year': year, 'limit': -1}, endpoint, 'get')

    page_header = "Visualization & Analytics"
    if response.status_code == 200:
        result = response.json()

        if request.is_ajax():
            return result

        total_data = int(result['total_count'])
        current_page = int(result["page"])
        total_pages = total_page_number(total_data, limit)
        # all_products_data_res = all_products_response.json()
        return {
            "active_page": "product-scatter",
            "years": get_all_active_year(request),
            "all_years": get_all_year(request),
            "items": result['data'],
            "product": product,
            # "all_items": all_products_data_res['data'],
            "page_header": page_header,
            "current_page": current_page,
            "total_pages": total_pages,
            "total_data": total_data,
            "year": int(year),
            "keyword": keyword,
            'start': settings.PERPAGE_DATA * current_page - settings.PERPAGE_DATA,
            "pagination_links": get_pagination_links(current_page, total_pages, "/visualization/product-family",
                                                     keyword, 'year', str(year)),
            "limit":limit
        }
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    return {
        "items": {},
        "years": get_all_active_year(request),
        "all_years": get_all_year(request),
        "page_header": page_header,
        "current_page": 0,
        "total_pages": 0,
        "total_data": 0,
        'start': 0,
        "year": int(year),
        'keyword': keyword
    }


# get_customer_by_year
def get_customer_by_year(request):
    endpoint = 'get-unique-customer'
    page = request.GET.get('page', 1)
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    customer = request.GET.get('customer', None)
    keyword = request.GET.get('keyword', customer)
    limit = -1
    prams = {'year': year, 'limit': limit, 'page': page}
    if keyword:
        prams.update({"keyword": keyword})

    response = get_api_server_response(
        request, prams, endpoint, 'get')

    page_header = "Visualization & Analytics"
    if response.status_code == 200:
        result = response.json()
        if request.is_ajax():
            return result
        total_data = int(result['total_count'])
        current_page = int(result["page"])
        total_pages = total_page_number(total_data, limit)
        return {
            "active_page": "customer-scatter",
            "years": get_all_active_year(request),
            "all_years": get_all_year(request),
            "items": result['data'],
            "page_header": page_header,
            "current_page": current_page,
            "total_pages": total_pages,
            "total_data": total_data,
            "year": int(year),
            "customer": customer,
            "keyword": keyword,
            'start': settings.PERPAGE_DATA * current_page - settings.PERPAGE_DATA,
            "pagination_links": get_pagination_links(current_page, total_pages, "/visualization/customers", keyword,
                                                     'year', str(year)),
            "limit":limit
        }
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    return {
        "items": {},
        "years": get_all_active_year(request),
        "all_years": get_all_year(request),
        "page_header": page_header,
        "current_page": 0,
        "total_pages": 0,
        "total_data": 0,
        'start': 0,
        "year": int(year),
        'keyword': keyword,
    }


# get_waterfall_chart_data_by_year
def get_waterfall_chart_data_by_year(request):
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    endpoint = 'get-waterfall-data'
    product = request.GET.get('product', None)
    customer = request.GET.get('customer', None)
    page_header = "Visualization & Analytics"
    active_page = "waterfall-chart"
    if product and customer:
        params = {
            "product_family": product,
            "customer": customer,
            "year": year
        }
        response = get_api_server_response(
            request, params, endpoint, 'get')
        if response.status_code == 200:
            result = response.json()
            return {
                "page_header": page_header,
                "years": get_all_active_year(request),
                "all_years": get_all_year(request),
                "active_page": active_page,
                "items": result,
                "year": year
            }
        elif response.status_code == 401:
            clear_login_session_data(request)
            return False
    return {
        "page_header": page_header,
        "years": get_all_active_year(request),
        "all_years": get_all_year(request),
        "active_page": active_page,
        "items": [],
        "year": year
    }


# get_scatter_plot_chart_data_by_year_with_pagination
def get_scatter_plot_chart_data_by_year_with_pagination(request):
    endpoint = 'get-paginated-scatterplot-data'
    page = request.GET.get('page', 1)
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    limit = -1
    params = {'year': year, 'page': page, 'limit': limit}
    response = get_api_server_response(
        request, params, endpoint, 'get')
    page_header = "Visualization & Analytics"
    if response.status_code == 200:
        result = response.json()
        total_data = int(result['total_count'])
        current_page = int(result["page"])
        total_pages = total_page_number(total_data, limit)
        return {
            'active_page': 'waterfall-chart',
            "items": result['data'],
            "years": get_all_active_year(request),
            "all_years": get_all_year(request),
            "year": int(year),
            "page_header": page_header,
            "current_page": current_page,
            "total_pages": total_pages,
            "total_data": total_data,
            'start': settings.PERPAGE_DATA * current_page - settings.PERPAGE_DATA,
            "pagination_links": get_pagination_links(current_page, total_pages, "/visualization/waterfall-chart"),
            "limit":limit
        }
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    return {
        "items": {},
        "years": get_all_active_year(request),
        "all_years": get_all_year(request),
        "page_header": page_header,
        "current_page": 0,
        "total_pages": 0,
        "total_data": 0,
        'start': 0,
    }


# get_histogram_data
def get_histogram_data(request):
    page = request.GET.get('page', 1)
    endpoint = 'get-paginated-pocket-price-band-histogram'
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    page_header = "Visualization & Analytics"
    active_page = "histogram"
    limit = -1
    params = {'year': year, 'page': page, 'limit': limit}
    response = get_api_server_response(
        request, params, endpoint, 'get')
    if response.status_code == 200:
        result = response.json()
        total_data = int(result['total_count'])
        current_page = int(result["page"])
        total_pages = total_page_number(total_data, limit)
        return {
            "page_header": page_header,
            "active_page": active_page,
            "items": result['data'],
            "years": get_all_active_year(request),
            "year": int(year),
            "all_years": get_all_year(request),
            "current_page": current_page,
            "total_pages": total_pages,
            "total_data": total_data,
            'start': settings.PERPAGE_DATA * current_page - settings.PERPAGE_DATA,
            "pagination_links": get_pagination_links(current_page, total_pages, "/visualization/histogram",
                                                     None, 'year', str(year))
        }
    elif response.status_code == 401:
        clear_login_session_data(request)
        return False
    return {
        "page_header": page_header,
        "active_page": active_page,
        "items": [],
        "years": get_all_active_year(request),
        "all_years": get_all_year(request),
        "year": int(year)
    }


# get_histogram_chart_data_by_year
def get_histogram_chart_data_by_year(request):
    endpoint = 'get-histogram-diagram'
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    threshold = request.GET.get('threshold', 5)
    params = {'year': year, 'threshold': threshold}
    response = get_api_server_response(request, params, endpoint, 'get')
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return []


# pie_dashboard_chart_data
def pie_dashboard_chart_data(request, year):
    params = {
        "year": year
    }
    response = get_api_server_response(request, params, 'get-piechart', 'get')
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        return {}


# get_scatter_plot_scatter_analyze_data
def get_scatter_plot_scatter_analyze_data(request):
    now = datetime.datetime.now()
    year = request.GET.get('year', now.year)
    product = request.GET.get('product', "")
    params = {
        "year": year,
        "product": product
    }
    response = get_api_server_response(request, params, 'calculation-data', 'get')
    if response.status_code == 200:
        result = response.json()
        table_data = result['data']
        return {
            "table_data": table_data
        }
    else:
        return {
            "table_data": []
        }
