from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

from services import FileService


class FilePrintEndpoint(HTTPEndpoint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_data = {
            'status_code': 400,
            'content': {
                'error': '',
            }
        }

    async def post(self, request):
        form = await request.form()
        if 'file' not in form:
            self.response_data['content']['error'] = 'invalid request, missing file'
            return JSONResponse(**self.response_data)

        try:
            data = await form['file'].read()
        except ValueError:
            self.response_data['content']['error'] = 'invalid request, incorrect file'
            return JSONResponse(**self.response_data)

        instance = await FileService.create_file(data=data)
        if not instance:
            self.response_data['content']['error'] = 'cannot create file, incorrect input data'

        await request.app.state.queue.put(instance)
        self.response_data['status_code'] = 201
        self.response_data['content']['file_id'] = str(instance.id)

        return JSONResponse(**self.response_data)
