import frappe
from frappe.utils.file_manager import save_file
import base64

@frappe.whitelist(allow_guest=False)
def update_user_image(image, filename=None):
    """Update the current user's profile image."""
    current_user = frappe.session.user

    # Decode Base64 image (if provided as base64)
    if image.startswith("data:image"):
        format, imgstr = image.split(";base64,")
        ext = format.split("/")[-1]
        image = base64.b64decode(imgstr)
        filename = filename or f"{current_user}_profile.{ext}"

    try:
        # Save file in Frappe File Manager
        file_doc = save_file(filename, image, "User", current_user, is_private=0)

        # Update user document with new image URL
        frappe.db.set_value("User", current_user, "user_image", file_doc.file_url)
        frappe.db.commit()

        return {
            "status": "success",
            "message": "Profile image updated successfully",
            "image_url": file_doc.file_url
        }
    except Exception as e:
        frappe.log_error(f"Profile image update error: {str(e)}", "update_user_image")
        return {"status": "error", "message": str(e)}
