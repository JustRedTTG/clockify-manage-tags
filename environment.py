import os

import dotenv

dotenv.load_dotenv()

api_key = os.getenv('API_KEY')

workspace_id = os.getenv('WORKSPACE_ID')
user_id = os.getenv('USER_ID')


paid_tag_id = os.getenv('PAID_TAG_ID')
unpaid_tag_id = os.getenv('UNPAID_TAG_ID')
