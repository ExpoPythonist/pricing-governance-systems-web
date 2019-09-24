from django.shortcuts import render, redirect, render_to_response
from django.http import JsonResponse, HttpResponse
from .service import *
import json


# scatter_plot
def scatter_plot(request):
    if is_logged_in(request):
        response = get_product_by_year(request)
        if request.is_ajax():
            return JsonResponse(response)
        if response is not False:
            return render(request, "visualization/scatter-plot/product-scatter-plot-chart.html", response)
        else:
            return redirect("scatter-plot")
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# scatter_plot_chart_data
def scatter_plot_chart_data(request):
    if is_logged_in(request):
        # response = get_scatter_plot_chart_data_by_year(request, 2018)
        year = request.GET.get('year', None)
        product = request.GET.get('product', None)
        customer = request.GET.get('customer', None)
        page_header = "Visualization & Analytics"
        if customer:
            active_page = "customer-scatter"
        else:
            active_page = "product-scatter"

        response = {
            "page_header": page_header,
            "active_page": active_page,
            "all_years": get_all_year(request),
            "product": product,
            "customer": customer,
            "year": year
        }
        if customer:
            page = "visualization/scatter-plot/customer-scatter-plot-chart-data.html"
        else:
            page = "visualization/scatter-plot/product-scatter-plot-chart-data.html"
        return render(request, page, response)
    messages.add_message(
        request, messages.ERROR, "Your login session is expired. Please login again.")
    return redirect('login')


# scatter_plot_chart_data_ajax
def scatter_plot_chart_data_ajax(request):
    if is_logged_in(request):
        response = get_scatter_plot_chart_data_by_year(request)
        customer = request.GET.get('customer', None)
        if customer:
            page = "visualization/scatter-plot/customer-scatter-data.html"
        else:
            page = "visualization/scatter-plot/product-scatter-data.html"
        return render(request, page, response)

    messages.add_message(
        request, messages.ERROR, "Your login session is expired. Please login again.")
    return redirect('login')


def customer_scatter_plot(request):
    if is_logged_in(request):
        response = get_customer_by_year(request)
        if request.is_ajax():
            return JsonResponse(response)
        if response is not False:
            return render(request, "visualization/scatter-plot/customer-scatter-plot-chart.html", response)
        else:
            return redirect("customer-scatter-plot")
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# scatter_plot
def waterfall_chart(request):
    if is_logged_in(request):
        response = get_scatter_plot_chart_data_by_year_with_pagination(
            request)
        if response is not False:
            return render(request, "visualization/waterfall/waterfall-chart.html", response)
        else:
            return redirect("waterfall-chart")
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# waterfall_chart_data
def waterfall_chart_data(request):
    if is_logged_in(request):
        response = get_waterfall_chart_data_by_year(request)
        if response is not False:
            return render(request, "visualization/waterfall/waterfall-chart-chart-data.html", response)
        else:
            return redirect("waterfall-chart-data")
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# get_histogram
def get_histogram(request):
    if is_logged_in(request):
        response = get_histogram_data(request)
        if response is not False:
            return render(request, "visualization/histogram/histogram-chart-chart-data.html", response)
        else:
            return redirect("histogram-chart")
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# get_histogram_chart_data
def get_histogram_chart_data(request):
    if is_logged_in(request):
        response = get_histogram_chart_data_by_year(request)
        return JsonResponse(response)
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')


# get_pie_chart_data
def get_pie_chart_data(request, year):
    response = pie_dashboard_chart_data(request, year)
    return JsonResponse(response, status=200)


# get_scatter_plot_analyze_data
def get_scatter_plot_analyze_data(request):
    if is_logged_in(request):
        response = get_scatter_plot_scatter_analyze_data(request)
        return render(request, "visualization/scatter-plot/scatter-plot-analyze_data.html", response)
    else:
        messages.add_message(
            request, messages.ERROR, "Your login session is expired. Please login again.")
        return redirect('login')

def ajax_product_scatterplot(request):
    if is_logged_in(request):
        # response = get_scatter_plot_chart_data_by_year(request, 2018)
        year = request.GET.get('year', None)
        product = request.GET.get('product', None)
        customer = request.GET.get('customer', None)
        page_header = "Visualization & Analytics"
        if customer:
            active_page = "customer-scatter"
        else:
            active_page = "product-scatter"

        response = {
            "page_header": page_header,
            "active_page": active_page,
            "all_years": get_all_year(request),
            "product": product,
            "customer": customer,
            "year": year
        }

        page = "visualization/scatter-plot/ajax-product-scatter-plot-chart-data.html"
        return render(request, page, response)

def ajax_product_waterfall(request):
    if is_logged_in(request):
        response = get_waterfall_chart_data_by_year(request)
        page = "visualization/waterfall/ajax-product-waterfall-chart-data.html"
        return render(request, page, response)

