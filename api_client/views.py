from django.shortcuts import render
from django.views import View
from .jsonrpc import JsonRpcClient

class JsonRpcView(View):
    def get(self, request):
        return render(request, 'api_client/form.html')

    def post(self, request):
        method = request.POST.get('method')
        params = request.POST.get('params', '').split(',')
        client = JsonRpcClient("https://slb.medv.ru/api/v2/")
        response = client.call_method(method, params)
        return render(request, 'api_client/form.html', {'response': response})
