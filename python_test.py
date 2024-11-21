'''
sql subquery concept and practice questions

Sure! A subquery is a SQL query nested inside another query. It can be used to perform operations that require multiple steps, 
allowing you to filter or aggregate data in a more complex way. Subqueries can be used in various places within a SQL statement, including:

In the SELECT clause: To derive a value for each row.
In the WHERE clause: To filter results based on the results of another query.
In the FROM clause: To treat the results of a query as a table.

Types of Subqueries
Single-row subquery: Returns a single row.
Multiple-row subquery: Returns multiple rows.
Correlated subquery: References columns from the outer query.

Examples
--------
Using a subquery in the WHERE clause:
SELECT employee_id, employee_name
FROM employees
WHERE department_id IN (SELECT department_id FROM departments WHERE location_id = 1000);

Using a subquery in the SELECT clause:
SELECT employee_id,
       (SELECT AVG(salary) FROM employees WHERE department_id = e.department_id) AS avg_salary
FROM employees e;

Using a correlated subquery:
SELECT e1.employee_id, e1.salary
FROM employees e1
WHERE e1.salary > (SELECT AVG(salary) FROM employees e2 WHERE e1.department_id = e2.department_id);

Practice Questions
Basic Subquery: Write a query to find all products with a price higher than the average price of all products.

Subquery in the FROM clause: Create a query that retrieves the total sales per product by using a subquery to calculate total sales.

Correlated Subquery: Find employees whose salary is greater than the average salary of their department.

Subquery with JOIN: Write a query that lists all employees and their department names, but only for those departments located in a specific city (e.g., "New York").

Not Exists: Write a query to find all customers who have not placed any orders.

select * from products
where price > (select AVG(price) from product)

SELECT p.product_name,
       (SELECT COUNT(s.product_id) FROM sales s WHERE s.product_id = p.product_id) AS total_sales
FROM products p;

select employee_id ,employee_name, employee_salary 
from employess e where salary > (select AVG(salary) where e.departent_id = d.department_id from department as d)
'''
# ---------------------------
'''
now in my view i have a create method. Now i want the create logic in serializer and in the view i only want to 
pass the data back to serilaizer and the data returned by the serializer to view and from view to the postman  my view code class CartItemPostSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemPostSerializer 
    permission_classes = [AllowAny]
    http_method_names = ['post']
    
    def create(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        cart_id = self.kwargs.get('cart_id')
        # Get or create the cart
        cart, created = Cart.objects.get_or_create(user=user, cart_id=cart_id)

        items_data = request.data.get('items', [])
        response_data_1 = []
        cart_items = []

        for item_data in items_data:
            item_serializer = CartItemPostSerializer(data=item_data)
            if item_serializer.is_valid():
                variant_id = item_data['variant']
                variant = get_object_or_404(ProductVariants, pk=variant_id) 
                
                cart_item = CartItem(
                    cart_id=cart,
                    variant=variant,
                    quantity=item_serializer.validated_data['quantity'],
                    price=variant.price
                )
                cart_items.append(cart_item)

                response_data_1.append({
                    "cart_id": cart.cart_id,
                    "created_at": cart.created_at,
                    "updated_at": cart.updated_at,
                    "variant": {
                        "variant_id": cart_item.variant.pk,
                        "variant_name": cart_item.variant.variant_name,
                        "variant_image": cart_item.variant.images.first().image.url if cart_item.variant.images.exists() else None,
                    },
                    "quantity": cart_item.quantity,
                    "price": cart_item.price,
                    "total_price": cart_item.calculate_price()
                })
            else:
                return Response({
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': item_serializer.errors,
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)

        # Bulk create cart items
        CartItem.objects.bulk_create(cart_items)

        response_data = {
            'cart_id': cart.cart_id,
            "created_at": cart.created_at,
            "updated_at": cart.updated_at,
            "user": user.username if user else None,
            "items": response_data_1
        }

        return Response({
            'status': status.HTTP_201_CREATED,
            'message': 'Items added to cart successfully.',
            'cart': response_data
        }, status=status.HTTP_201_CREATED) and my srilaizer class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)
    user = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['cart_id', 'created_at', 'updated_at', 'user','cart_items']
    
    def get_created_at(self, obj):
        """
        This function converts timestamp in ISO 8601 format to a properly formatted datetime string.
        """
        if obj.created_at:
            local_time = timezone.localtime(obj.created_at)
            return local_time.strftime('%Y-%m-%d %H:%M:%S')
        return 'None'
    
    def get_user(self, obj):
        user_info = obj.user
        if user_info:
          return {
            'id': user_info.id,
            'user_name': user_info.username,
          }
        return None

class CartItemPostSerializer(serializers.ModelSerializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariants.objects.all(), write_only=True)
    quantity = serializers.IntegerField(required=False, default=1)
    
    class Meta:
        model = CartItem
        fields = ['variant', 'quantity']
    
    def validate_quantity(self, value):
        if value is None:
            raise CustomValidation("Quantity is required",)
        if value < 1:
            raise CustomValidation("Quantity must be at least 1.", status_code=status.HTTP_400_BAD_REQUEST)
        elif value > 5:
            raise CustomValidation("Quantity can't be at more than 5", status_code=status.HTTP_400_BAD_REQUEST)
        return value
    
    def validate(self, data):
        print('qwe',data)
        variant_id = data.get('variant')
        print('var-id',variant_id.pk)
        variant = ProductVariants.objects.filter(pk=variant_id.pk).exists()
        
        if not variant:
            raise CustomValidation("No product with the given ID was found.")

        # if not variant.is_active:
        #     raise CustomValidation("The selected variant is out of stock.")
        
        return data
'''

'''
#########################################################################################################################################################
This search on google: single vaidation method for all the char field across all the models in django 
got me here: https://stackoverflow.com/questions/1624782/django-model-fields-validation

---------------------------------------------------------------
Do Not Delete. Search on chatgpt coz its a important concept 
--------------------------------------------------------------

Django has a model validation system in place since version 1.2.

In comments sebpiq says "Ok, now there is a place to put model validation ... except that it is run only when using a ModelForm! 
So the question remains, when it is necessary to ensure that validation is respected at the db-level, what should you do? Where to call full_clean?"

It's not possible via Python-level validation to ensure that validation is respected on the db level. 
The closest is probably to call full_clean in an overridden save method. This isn't done by default, 
because it means everybody who calls that save method had now better be prepared to catch and handle ValidationError.

But even if you do this, someone can still update model instances in bulk using queryset.update(), which will bypass this validation. 
There is no way Django could implement a reasonably-efficient queryset.update() that could still perform Python-level validation on every updated object.

The only way to really guarantee db-level integrity is through db-level constraints; any validation you do through the ORM requires 
the writer of app code to be aware of when validation is enforced (and handle validation failures).

This is why model validation is by default only enforced in ModelForm - because in a ModelForm there is already an obvious way to handle a ValidationError.
###############################################################################################################################################################################
def partial_update(self, request, cart_id=None):
        # Retrieve the cart or raise a 404 if not found
        cart = get_object_or_404(Cart, cart_id=cart_id)
        
        # Retrieve the variant_id and quantity from the request data
        variant_id = request.data.get('variant')
        if not variant_id:
            return error_response("Variant ID is required", status.HTTP_400_BAD_REQUEST)
        
        # Retrieve the variant or raise a 404 if not found
        variant = get_object_or_404(ProductVariants, id=variant_id)
        # try:
        #     variant = get_object_or_404(ProductVariants, id=variant_id)
        # except Exception as e:
        #     return Response({'test':'from views in cart'})
        # Retrieve quantity from request data and validate it
        quantity = request.data.get('quantity', 1)  # Default to 1 if quantity is not provided
        
        # Use the serializer to either create or update the cart item
        serializer = self.serializer_class()
        try:
            cart_item = serializer.create_or_update_cart_item(cart, variant, quantity)
            
            # If cart_item is None, it was deleted
            if cart_item == "Deleted":
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Cart item removed successfully.',
                    'data': []
                }, status=status.HTTP_200_OK)
            
            if cart_item == "NotFound":
                return Response({
                    'status': status.HTTP_200_OK,
                    'message': 'Cart item not found.',
                    'data': []
                }, status=status.HTTP_200_OK)

            serialized_data = self.serializer_class(cart_item)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Quantity updated successfully',
                'data': serialized_data.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
'''

# import re

# text = 'Ashutoshverma'
# regex = '^[a-zA-Z ]+$' 

# x = re.match(regex, text)
# if x:
#     print("Match found:", x.group())  # x.group() will return the matched string
# else:
#     print("No match found")
    
# print('cart_01bOmkvbW9CeUx'.count())