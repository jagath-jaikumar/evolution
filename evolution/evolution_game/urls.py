"""
URL configuration for evolution_game project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path

from evolution.evolution_core.views import router as core_router
from evolution.evolution_game.settings import DEBUG
from evolution.evolution_game.views import (liveness_check, readiness_check,
                                            root)

urlpatterns = [
    # administration
    path("admin/", admin.site.urls),
    path("probes/liveness/", liveness_check),
    path("probes/readiness/", readiness_check),
    # app
    path("", root),
    path("api/", include(core_router.urls)),
]
