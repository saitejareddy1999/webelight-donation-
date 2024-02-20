from django.urls import path

from number import views

urlpatterns = [
    # path('payment/', views.number_view, name = 'payment'),

    path('payment/', views.payment, name = 'payment'),
    path('History/', views.History, name="history"),
    path('handlerequest/', views.handlerequest, name = 'handlerequest'),

]
