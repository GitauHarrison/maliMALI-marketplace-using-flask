import json
import requests
from flask import request
import ipinfo
from app import app


def get_user_location():
    handler = ipinfo.getHandler(app.config['IP_INFO_ACCESS_TOKEN'])
    # Get address if user is using a proxy
    # Alternatively use their remote address
    # ip_user = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    # ip_user = '216.239.36.21'
    ip_user = request.environ.get('HTTP_X_FORWARDED_FOR')
    print(ip_user)
    details = handler.getDetails(ip_user)
    return details
