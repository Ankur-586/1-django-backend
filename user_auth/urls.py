from django.urls import path,include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserViewSet
from .utils import CustomTokenObtainPairView

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('user-token/',ObtainTokenView.as_view(),name='user-token'),
]



# http://127.0.0.1:8000/auth/users/reg  
# http://127.0.0.1:8000/product/products

'''
A company wants to contact each of its customers regarding the policy changes. They have international customers, but their database does not include country codes with their phone numbers.
There are two tables in the database: customers country_codes. The first table contains details of every customer including customerid, namephone_number,country
. The second table contains the country code for every country.
Write a query to retrieve a list of all customer ids, names, and phone numbers, with their country codes concatenated with their phone numbers. Sort the output in the order of their 

SELECT 
    customer_id, 
    name, 
    CONCAT('+',
        (SELECT country_code FROM country_codes WHERE country_codes.country = customers.country), 
        phone_number
    ) AS full_phone_number
FROM 
    customers
ORDER BY 
    customer_id;
    
    A stock is considered profitable if the predicted price is strictly greater than the current price. Write a query to find the stock_codes of all the stocks which are profitable based on this definition. Sort the output in ascending order.
There are two tables in the database: <em>price_today </em> and  <em>price_tomorrow.</em>&nbsp;Their primary keys are <em>stock_code</em>
'''