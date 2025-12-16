import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # settings.LOGIN_EXEMPT_URLS를 컴파일된 정규식 리스트로 저장
        self.exempt_urls = [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

    def __call__(self, request):
        assert hasattr(request, 'user'), (
            "LoginRequiredMiddleware requires authentication middleware to be installed. "
            "Edit your MIDDLEWARE setting to add 'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )

        path = request.path_info.lstrip('/')
        
        # 예외 URL에 포함되는지 확인
        for url_pattern in self.exempt_urls:
            if url_pattern.match(path):
                return self.get_response(request)
        
        # 예외 URL에 포함되지 않고, 로그인도 되어있지 않다면 로그인 페이지로 리다이렉트
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        response = self.get_response(request)
        return response

    