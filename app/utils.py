import asyncio
from pydoc import locate


def register_pipeline(app, services):
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    first_queue = asyncio.Queue(loop=loop)

    @app.on_event('startup')
    async def start_pipeline():
        output_queue = None
        for service in services:
            input_queue = output_queue or first_queue
            output_queue = asyncio.Queue(loop=loop)

            service = locate(service)
            if not service:
                continue

            asyncio.ensure_future(service(input_queue=input_queue,
                                          output_queue=output_queue).start(),
                                  loop=loop)
            input_queue = output_queue

    return first_queue