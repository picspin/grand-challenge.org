# -*- coding: utf-8 -*-
from django.urls import path

from grandchallenge.minioupload.views import presigned_url, MinioFileUpload, \
    EvaporateFileUpload, presign_string

urlpatterns =[
    path('presign/<path:filename>/', presigned_url),
    path('presign/', presign_string),
    path('upload/', MinioFileUpload.as_view()),
    path('evaporate/', EvaporateFileUpload.as_view()),
]
