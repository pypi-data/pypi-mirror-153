from django.urls import include, path

from obpages.accounts import views

urlpatterns = [
    path("account", views.ManageAccountView.as_view(), name="manage_account"),
    path(
        "account/",
        include(
            [
                path("login", views.CustomLoginView.as_view(), name="login"),
                path("logout", views.CustomLogoutView.as_view(), name="logout"),
                path("create", views.CustomCreateView.as_view(), name="create"),
                path("create/done", views.CreateDoneView.as_view(), name="create_done"),
                path(
                    "password_change",
                    views.CustomPasswordChangeView.as_view(),
                    name="password_change",
                ),
                path(
                    "password_change/done",
                    views.CustomPasswordChangeDoneView.as_view(),
                    name="password_change_done",
                ),
                path(
                    "password_reset",
                    views.CustomPasswordResetView.as_view(),
                    name="password_reset",
                ),
                path(
                    "password_reset/done",
                    views.CustomPasswordResetDoneView.as_view(),
                    name="password_reset_done",
                ),
                path(
                    "reset/<uidb64>/<token>",
                    views.CustomPasswordResetConfirmView.as_view(),
                    name="password_reset_confirm",
                ),
                path(
                    "reset/done",
                    views.CustomPasswordResetCompleteView.as_view(),
                    name="password_reset_complete",
                ),
            ]
        ),
    ),
]
