from rest_framework.test import APITestCase

from .models import Cart
from user_auth.models import CustomUser
from .serializers import CartItemPostSerializer

class CarSerilaizerTestCase(APITestCase):
    def test_cart_serializers(self):
        data = {
                "items": [
                    {
                        "variant": 1,
                        "quantity": 3
                    },
                    {
                        "variant": 5,
                        "quantity": 5
                    }
                ]
            }
        serializer = CartItemPostSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        # Assert that there are no validation errors
        self.assertFalse(serializer.errors)
        validated_data = serializer.validated_data
        self.assertEqual(len(validated_data['items']), 2)
        self.assertEqual(validated_data['items'][0]['variant'], self.variant1)
        self.assertEqual(validated_data['items'][1]['variant'], self.variant2)
        
        self.assertTrue(serializer.is_valid())
        self.assertFalse(serializer.errors)
    
    