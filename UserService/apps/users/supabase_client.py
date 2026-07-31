import uuid 
from supabase import create_client
from django.conf import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

def upload_to_supabase(file, bucket: str= "profile-pictures")-> str:
    file_bytes = file.read()
    extension=file.name.split(".")[-1]
    unique_name=f"{uuid.uuid4()}.{extension}"

    supabase.storage.from_(bucket).upload(
        path=unique_name,
        file=file_bytes,
        file_options={"content-type": file.content_type}
    )

    return supabase.storage.from_(bucket).get_public_url(unique_name)