from django.urls import path

from async_notifications.views import updatenewscontext, fromnewscontext, preview_email_newsletters, search_email

urlpatterns = [
    path('search_email', search_email, name="search_email"),
    path('context/<int:pk>', updatenewscontext, name="updatenewscontext"),
    path('context/<int:pk>/form', fromnewscontext),
    path('context/<int:pk>/preview', preview_email_newsletters, name='preview_newsletter_emails')
]