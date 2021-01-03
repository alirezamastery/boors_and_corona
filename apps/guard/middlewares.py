from django.http import JsonResponse

from django.core.cache import cache
from django.urls import resolve
from django.utils import timezone
from rest_framework import status

from .models import BlockedIp, SecurityConfig, ViewDetail

from .utils import get_client_ip


class BlockIpMiddleware:
    maximum_rps = 4
    timeout = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        view, _, _ = resolve(request.path)
        user_ip = get_client_ip(request)

        response = self.banned_before(user_ip)
        print('was blocked before', response)
        if response:
            # return response
            return JsonResponse({'error': 'Too many requests!'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            # response = self.get_response(request)
            # print(response.__dict__)
            # return JsonResponse(status.HTTP_429_TOO_MANY_REQUESTS , safe=False)

        LIMITED_VIEWS = SecurityConfig.objects.last().views.values_list(
                'name',
                flat=True)

        # Your code
        ip_request_time = cache.set(f'{user_ip}_{timezone.now()}', timezone.now(), timeout=self.timeout)
        # print(f'ip_request_time: {ip_request_time}')
        # print(f'view: {view}')
        # print(f'request.path: {request.path}')

        rps = self.validate_request_per_second(user_ip, request.path, request)
        if rps > 4:
            print('rps is more than 4')
            view_detail = ViewDetail.objects.filter(path=request.path).first()
            # blocked_ip , created = BlockedIp.objects.update_or_create(ip=user_ip, view=view_detail, rps=rps)
            blocked_ip = BlockedIp.objects.create(ip=user_ip, view=view_detail, rps=rps)
            blocked_ip.save()
            return JsonResponse({'error': 'Too many requests!'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # -----------------
        response = self.get_response(request)

        return response

        pass

    def banned_before(self, user_ip):
        return BlockedIp.is_ip_blocked(user_ip)

    def validate_request_per_second(self, user_ip, url_path, data):
        requests = cache.get_many(cache.keys(f'{user_ip}*'))
        requests = sorted(list(requests.values()), reverse=True)

        time_0 = requests[0]
        rs = 0
        for r in requests:
            print(r, (time_0 - r).total_seconds())
            if (time_0 - r).total_seconds() > 1:
                break
            rs += 1
        print(rs)
        return rs
