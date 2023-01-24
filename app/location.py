import json
import requests
from flask import request
import ipinfo
from app import app


def get_user_location():
    handler = ipinfo.getHandler(app.config['IP_INFO_ACCESS_TOKEN'])
    # ip_user = request.remote_addr
    ip_user = '216.239.36.21'
    details = handler.getDetails(ip_user)
    return details
