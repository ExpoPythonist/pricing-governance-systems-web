"""pricing_gov_sys_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf.urls import url
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path(r'product-family', views.scatter_plot, name="scatter-plot"),
    path(r'scatter-plot-chart', views.scatter_plot_chart_data, name="scatter-plot-data"),
    path(r'scatter-plot-chart-ajax', views.scatter_plot_chart_data_ajax, name="scatter-plot-data-ajax"),

    path(r'ajax/product-scatterplot', views.ajax_product_scatterplot, name="ajax-product-scatterplot"),
    path(r'ajax/product-waterfall', views.ajax_product_waterfall, name="ajax-product-waterfall"),

    path(r'customers', views.customer_scatter_plot, name="customer-scatter-plot"),

    # Waterfall char data
    path(r'waterfall-chart', views.waterfall_chart, name="waterfall-chart"),
    path(r'waterfall-chart-generate', views.waterfall_chart_data, name="waterfall-chart-data"),

    # Histogram
    path(r'histogram', views.get_histogram, name="histogram-chart"),
    path(r'histogram-chart', views.get_histogram_chart_data, name="histogram-chart-data"),
    path(r'scatter-plot-analysis-data', views.get_scatter_plot_analyze_data, name="scatter-plot-analysis-data"),

    # Dashboard pie chart
    path(r'get-pie-chart-data/<int:year>', views.get_pie_chart_data, name="dashboard-pie-chart-data"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += staticfiles_urlpatterns()
