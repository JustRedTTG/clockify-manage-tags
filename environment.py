import os

import dotenv

dotenv.load_dotenv()

api_key = os.getenv('API_KEY') or None

workspace_id = os.getenv('WORKSPACE_ID') or None
user_id = os.getenv('USER_ID') or None


paid_tag_id = os.getenv('PAID_TAG_ID') or None
unpaid_tag_id = os.getenv('UNPAID_TAG_ID') or None
