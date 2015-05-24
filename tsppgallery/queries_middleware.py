from django.db import connection

class QueriesMiddleware:
    def process_request(self, request):
        connection.queries.clear()

    def process_response(self, request, response):
        for query in connection.queries:
            print(query)
        return response
