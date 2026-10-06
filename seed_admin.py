import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hiraya_project.settings')
django.setup()

from django.contrib.auth.models import User

# Admin staff accounts
ADMIN_USERS = [
    {"username": "amdesepeda", "email": "amdesepeda@student.hau.edu.ph"},
    {"username": "asmeneses", "email": "asmeneses1@student.hau.edu.ph"},
    {"username": "omgarcia", "email": "omgarcia@student.hau.edu.ph"},
    {"username": "cmgalang", "email": "cmgalang3@student.hau.edu.ph"},
    {"username": "zggarcia", "email": "zggarcia@student.hau.edu.ph"}
]

SHARED_PASSWORD = "HirayaAdmin2026!"

for admin_data in ADMIN_USERS:
    user, created = User.objects.get_or_create(
        username=admin_data["username"],
        defaults={"email": admin_data["email"]}
    )
    user.email = admin_data["email"]
    user.set_password(SHARED_PASSWORD)
    user.is_staff = True        # Grants Admin access
    user.is_superuser = True    # Grants full permissions
    user.save()

    if created:
        print(f"Created admin account: {admin_data['username']} ({admin_data['email']})")
    else:
        print(f"Updated admin account: {admin_data['username']} ({admin_data['email']})")

print("\nAll initial admin accounts are ready with the shared password!")