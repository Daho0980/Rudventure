"""
Global Functions 중 OSRelated 옵션

    ``slash`` : 파일의 주소를 불러올 때 사용하는 핵심 함수, OS에 따라 달라짐
"""

import os

def slash():
    """
    파일의 주소를 불러올 때 사용하는 핵심 함수, OS에 따라 달라짐
    """
    if os.name == 'posix': return '/'
    else                 : return '\\'