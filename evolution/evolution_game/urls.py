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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from evolution.evolution_core.views import router as core_router
from evolution.evolution_game.views import (
    get_user_id_from_username,
    liveness_check,
    readiness_check,
    register_user,
    root,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Evolution API",
        default_version="v1",
        description="Evolution API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("probes/liveness/", liveness_check),
    path("probes/readiness/", readiness_check),
    path("", root),
    path("api/", include(core_router.urls)),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("accounts/", include("django.contrib.auth.urls")),
    path("register/", register_user, name="register_user"),
    path("get_user_id/", get_user_id_from_username, name="get_user_id_from_username"),
]
