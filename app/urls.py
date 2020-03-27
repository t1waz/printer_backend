from starlette.routing import Route

import views


routes = [
    Route('/print_file', endpoint=views.FilePrintEndpoint, methods=['POST']),
]