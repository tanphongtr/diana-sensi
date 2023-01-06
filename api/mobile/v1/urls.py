"""bms_crawl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page

from .common import (
    ProvinceAPIView, SystemAPIView, MarketAPIView, ProvinceSystemMarketAPIView)
from .file import FileAPIView
from .product import ProductAPIView
from .gift import GiftAPIView
from .survey_question import SurveyQuestionAPIView
from .daily_gift import DailyGiftAPIView, BillListAPIView
from .customer import CustomerAPIView
from .lucky import LuckyAPIView

urlpatterns = [
    path('commons/provinces/', (ProvinceAPIView.as_view())),
    path('commons/systems/', (SystemAPIView.as_view())),
    path('commons/markets/', (MarketAPIView.as_view())),
    path('commons/provinces/nested/', (ProvinceSystemMarketAPIView.as_view())),


    path('files/', (FileAPIView.as_view())),


    path('products/', (ProductAPIView.as_view())),
    path('gifts/', (GiftAPIView.as_view())),
    path('survey_questions/', (SurveyQuestionAPIView.as_view())),
    path('daily_gifts/', (DailyGiftAPIView.as_view())),
    path('customers/', (CustomerAPIView.as_view())),
    path('lucky/', (LuckyAPIView.as_view({'post': 'get_lucky'}))),
    path('bills/', (BillListAPIView.as_view({'get': 'bill_list'}))),
]
