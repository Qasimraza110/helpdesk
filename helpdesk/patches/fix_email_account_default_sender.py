import frappe


def execute():
    """Patch EmailAccount.default_sender to handle None email_id"""
    from frappe.email.doctype.email_account.email_account import EmailAccount

    # Store original method
    original_default_sender = EmailAccount.default_sender

    # Define new property
    @property
    def patched_default_sender(self):
        import email.utils
        email_id = self.get("email_id")
        name = self.name or "Helpdesk"
        if not email_id:
            return name
        try:
            return email.utils.formataddr((name, email_id))
        except (TypeError, AttributeError):
            return name

    # Replace the property
    EmailAccount.default_sender = patched_default_sender
