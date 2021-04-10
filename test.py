from requests import get, post

print(get('http://localhost:8080/api/v2/users').json())
print(get('http://localhost:8080/api/v2/users/2').json())
print(get('http://localhost:8080/api/v2/orders').json())
print(get('http://localhost:8080/api/v2/orders/2').json())
print(get('http://localhost:8080/api/v2/products').json())
print(get('http://localhost:8080/api/v2/products/2').json())
print(get('http://localhost:8080/api/v2/order_details').json())
print(get('http://localhost:8080/api/v2/order_details/2/2').json())
print(get('http://localhost:8080/api/v2/basket').json())
print(get('http://localhost:8080/api/v2/basket/2/1').json())
