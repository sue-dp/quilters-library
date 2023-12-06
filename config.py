import os


group_name = "super-group"

su_first_name = "Super"
su_last_name = "Admin"
su_email = "superadmin@test.com"


users = [
    "Sue Roy",
    "Samantha Weaver",
    "Vicki Hutchings",
    "Jerusha Beckstead",
    "Mary Halvorson",
    "Pam Tuft"
]

groups = [
    "Hobble Creek Quilt Group",
    "Fabric Mill Friends"
]

roles = [
    "admin",
    "user"
]

s3_region = os.getenv("S3_REGION")
s3_endpoint = os.getenv("S3_ENDPOINT")
s3_public_bucket = os.getenv("PUBLIC_BUCKET")
s3_private_bucket = os.getenv("PRIVATE_BUCKET")
s3_private_app_key = os.getenv("PRIVATE_APP_KEY")
s3_public_app_key = os.getenv("PUBLIC_APP_KEY")
s3_private_key_id = os.getenv("PRIVATE_KEY_ID")
s3_public_key_id = os.getenv("PUBLIC_KEY_ID")
s3_private_key_name = os.getenv("PRIVATE_KEY_NAME")
s3_public_key_name = os.getenv("PUBLIC_KEY_NAME")

# Datastore selection ("server", "firebase", "cloudinary", "s3")
data_store = "s3"

# s3_storage_type can be set to "private" or "public"
s3_storage_type = "public"
