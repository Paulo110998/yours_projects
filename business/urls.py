from django.urls import path
from business.models import Negocio, Pipeline
from . views import CreateNegocio, CreatePipeline, UpdateNegocio, UpdatePipeline, DeleteNegocio, DeletePipeline, NegocioList, PipelineList, export_chart
from . import views 

urlpatterns = [
    path('create_business', CreateNegocio.as_view(), name='create-business'),
    path('update_business/<int:pk>/', UpdateNegocio.as_view(queryset=Negocio.objects.all()), name='update-business'),
    path('delete_business/<int:pk>/', DeleteNegocio.as_view(queryset=Negocio.objects.all()), name='delete-business'),
    path('your_business', NegocioList.as_view(queryset=Negocio.objects.all()), name='your-business'),
    path('customer_report', views.Negocios, name="customer-report"),
    #path('chart_sales', Negociochart.as_view(), name='sales'),
    
    path('chart_sales', views.quantidade_negocio, name="sales"),
    path('chart_export', views.export_chart, name="export"),

    path('create_pipeline', CreatePipeline.as_view(), name='create-pipeline'),
    path('update_pipeline/<int:pk>/', UpdatePipeline.as_view(queryset=Pipeline.objects.all()), name='update-pipeline'),
    path('delete_pipeline/<int:pk>/', DeletePipeline.as_view(queryset=Pipeline.objects.all()), name='delete-pipeline'),
    path('your_pipeline', PipelineList.as_view(queryset=Pipeline.objects.all()), name='pipeline'),
    
]