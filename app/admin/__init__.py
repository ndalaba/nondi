from flask import Blueprint
from app.entity.Message import Message
from flask_login import current_user
from sqlalchemy import text

admin = Blueprint('admin', __name__)


@admin.context_processor
def inject_mail():
    emails = Message.query.filter_by(user_id=current_user.id, read=False,folder='INBOX').order_by(text('created_at DESC')).all()
    return dict(unread_mails=emails, email_count=len(emails))


from . import profils
from . import messages
from . import categories
