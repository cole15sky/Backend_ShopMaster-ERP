from django.contrib.auth import get_user_model

User = get_user_model()

# List of seed users
seed_users = [
    {
        "email": "admin@shop.com",
        "password": "password",
        "full_name": "Admin User",
        "role": "ADMIN",
        "phone": "9800000001",
    },
    {
        "email": "staff1@shop.com",
        "password": "password",
        "full_name": "Shop Staff 1",
        "role": "STAFF",
        "phone": "9800000002",
    },
    {
        "email": "staff2@shop.com",
        "password": "password",
        "full_name": "Shop Staff 2",
        "role": "STAFF",
        "phone": "9800000003",
    },
    {
        "email": "customer1@shop.com",
        "password": "password",
        "full_name": "Customer 1",
        "role": "CUSTOMER",
        "phone": "9800000004",
    },
    {
        "email": "customer2@shop.com",
        "password": "password",
        "full_name": "Customer 2",
        "role": "CUSTOMER",
        "phone": "9800000005",
    },
]

for u in seed_users:
    if not User.objects.filter(email=u["email"]).exists():
        user = User.objects.create_user(
            email=u["email"],
            password=u["password"],
            full_name=u["full_name"],
            role=u["role"],
            phone=u["phone"]
        )
        print(f"Created user: {user.email}")
    else:
        print(f"User already exists: {u['email']}")