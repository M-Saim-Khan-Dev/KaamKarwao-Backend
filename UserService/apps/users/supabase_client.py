import uuid 
import logging
from supabase import create_client
from django.conf import settings

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
logger = logging.getLogger(__name__)

def upload_to_supabase(file, bucket: str= "profile-pictures")-> str:
    logger.info("Uploading profile image to object storage bucket=%s filename=%s", bucket, file.name)
    file_bytes = file.read()
    extension=file.name.split(".")[-1]
    unique_name=f"{uuid.uuid4()}.{extension}"

    try:
        supabase.storage.from_(bucket).upload(
            path=unique_name,
            file=file_bytes,
            file_options={"content-type": file.content_type}
        )
    except Exception:
        logger.exception("Profile image upload failed bucket=%s object=%s", bucket, unique_name)
        raise

    logger.info("Profile image upload completed bucket=%s object=%s", bucket, unique_name)
    return supabase.storage.from_(bucket).get_public_url(unique_name)
