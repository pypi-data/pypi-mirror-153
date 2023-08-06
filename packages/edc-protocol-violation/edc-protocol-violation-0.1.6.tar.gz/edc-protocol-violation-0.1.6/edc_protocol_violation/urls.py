from django.urls import path
from django.views.generic import RedirectView

app_name = "edc_protocol_violation"

urlpatterns = [
    path("", RedirectView.as_view(url="/edc_protocol_violation/admin/"), name="home_url"),
]
