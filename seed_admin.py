import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hiraya_project.settings')
django.setup()

from django.contrib.auth.models import User

# Admin staff accounts using email addresses
ADMIN_USERS = [
    {"email": "amdesepeda@student.hau.edu.ph"},
    {"email": "asmeneses1@student.hau.edu.ph"},
    {"email": "omgarcia@student.hau.edu.ph"},
    {"email": "cmgalang3@student.hau.edu.ph"},
    {"email": "zggarcia@student.hau.edu.ph"}
]

SHARED_PASSWORD = "hiraya2026"

for admin_data in ADMIN_USERS:
    email = admin_data["email"].strip()
    # Generate username from prefix before @
    generated_username = email.split("@")[0]

    # Find existing user by email or fallback to generated username
    user = User.objects.filter(email__iexact=email).first()
    if not user:
        user = User.objects.filter(username__iexact=generated_username).first()

    if not user:
        user = User.objects.create_user(
            username=generated_username,
            email=email,
            password=SHARED_PASSWORD
        )
        created = True
    else:
        created = False
        user.email = email
        user.set_password(SHARED_PASSWORD)

    user.is_staff = True        # Grants Admin access
    user.is_superuser = True    # Grants full permissions
    user.save()

    if created:
        print(f"Created admin account: {email}")
    else:
        print(f"Updated admin account: {email}")

print("\nAll initial admin accounts are ready with email authentication!")