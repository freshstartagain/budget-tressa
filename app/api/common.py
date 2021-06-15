from .. services.response_handler import success, error
from . import api

@api.route('/health-check', methods=['GET'])
def health_check():
     try:
         return success(data="OK", status_code=200)
         
     except Exception as e:
         return error(data={"error":e})
