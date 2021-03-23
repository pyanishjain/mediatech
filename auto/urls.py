from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from users import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name='index'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path("signup", views.signup, name='signup'),
    path('profile', views.profileList.as_view(), name='profile'),
    path("updateWithTokenProfile", views.updateWithTokenProfile,
         name='updateWithTokenProfile'),
    path("downloadSoftware/<str:name>",
         views.downloadSoftware, name='downloadSoftware'),
    path("plan_detail/", views.plan_detail, name="plan_detail"),
    path("contact/", views.contact, name="contact"),

    path("updateSoftware/", views.updateSoftware, name='updateSoftware'),
    path("login_user/", views.login_user, name="login_user"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("update/<int:id>/<str:api>", views.update, name="update"),

    # IPS
    path("createIP/<str:api>", views.createIP, name='createIP'),
    path("serverDateAPI/", views.serverDateAPI, name="serverDateAPI"),
    path("IpAPI/<str:api>", views.IpAPI, name="IpAPI"),
    path('telegramAPI/', views.telegramAPI, name='telegramAPI'),
    path('whatsappAPI/', views.whatsappAPI, name='whatsappAPI'),
    path('instagramAPI/', views.instagramAPI, name='instagramAPI'),

    path('variableAPI/<str:api>', views.variableAPI, name='variableAPI'),







    # Password

    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
