"""
URL configuration for hr project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hr_master.views import *
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular_extras.views import SpectacularScalarView
from hr_dump.views import metrics_view

router = DefaultRouter()


# HR_MASTER
router.register(r'master/company', CompanyViewSet)
router.register(r'master/unit', UnitViewSet)
router.register(r'master/level', LevelViewSet)
router.register(r'master/employment-type', EmploymentTypeViewSet)
router.register(r'master/shift', ShiftViewSet)
router.register(r'master/branch', BranchViewSet)
router.register(r'master/employee', EmployeeViewSet)

# HR_TRANSACTION

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hr/', include(router.urls)),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/scalar/', SpectacularScalarView.as_view(url_name='schema'), name='scalar-ui'),

    path('metrics/', metrics_view, name='metrics'),
]
