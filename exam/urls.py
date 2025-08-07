from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_exam_view, name='upload_exam'),  # Main upload page
    path('exam/', views.exam_view, name='exam'),            # Exam page
    path('submit/', views.submit_exam_view, name='submit_exam'),  # Submit exam
    path('result/', views.result_view, name='result'),      # Show result
    path('download_pdf/', views.download_result_pdf, name='download_pdf'), 
]
