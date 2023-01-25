import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """All application configurations"""

    # Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'difficult-password-to-guess'

    # Database configurations
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Image
    VENDOR_UPLOAD_PATH = os.environ.get('VENDOR_UPLOAD_PATH')

    # Mpesa Integration
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY')
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET')
    MPESA_API_URL = os.environ.get('MPESA_API_URL')
    MPESA_PARTY_A = os.environ.get('MPESA_PARTY_A')
    MPESA_PARTY_B = os.environ.get('MPESA_PARTY_B')
    MPESA_PHONE_NUMBER = os.environ.get('MPESA_PHONE_NUMBER')
    MPESA_BUSINESS_SHORT_CODE = os.environ.get('MPESA_BUSINESS_SHORT_CODE')
    MPESA_PASS_KEY = os.environ.get('MPESA_PASS_KEY')
    MPESA_INITIATOR_PASSWORD = os.environ.get('MPESA_INITIATOR_PASSWORD')
    MPESA_INITIATOR_NAME = os.environ.get('MPESA_INITIATOR_NAME')
    MPESA_BASIC_AUTHORIZATION = os.environ.get('MPESA_BASIC_AUTHORIZATION')
    MPESA_GRANT_TYPE = os.environ.get('MPESA_GRANT_TYPE')

    # IP Info
    IP_INFO_ACCESS_TOKEN = os.environ.get('IP_INFO_ACCESS_TOKEN')

    # Africa's talking API
    AFRICASTALKING_API_KEY = os.environ.get('AFRICASTALKING_API_KEY')
    AT_USERNAME = os.environ.get('AT_USERNAME')
