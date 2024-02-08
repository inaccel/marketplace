import fastapi
import gradio
import inaccel.coral as inaccel
import numpy as np
import os
import subprocess

from inaccel.gzip import compress

api = fastapi.FastAPI()


class BinaryResponse(fastapi.Response):

    def render(self, content):
        return content


@api.post('/')
async def gzip(request: fastapi.Request) -> fastapi.Response:
    with inaccel.allocator:
        _body = np.ndarray(0, dtype=np.ubyte)
    async for _chunk in request.stream():
        if len(_chunk) > 0:
            _body.resize(len(_body) + len(_chunk))
            _body[-len(_chunk):] = np.frombuffer(_chunk, dtype=np.ubyte)
    return BinaryResponse(compress(_body.data))


def fn(file):
    with open(file.name + '.gz', 'wb') as _compressed_file:
        with inaccel.allocator:
            _file = np.fromfile(file.name)
        _compressed_file.write(compress(_file.data))
    return _compressed_file.name


with gradio.Blocks(analytics_enabled=False, title='Gzip') as blocks:
    gradio.Markdown(
        value='<h1 style="text-align: center; margin-bottom: 1rem">' +
        blocks.title + '</h1>')
    gradio.Markdown(
        value=
        'Gzip (**GNU zip**) is a *compression utility* designed to be a replacement for "compress". Its main advantages over compress are much **better compression and freedom** from patented algorithms. The GNU Project uses it as the standard compression program for its system.'
    )
    with gradio.Row():
        with gradio.Column():
            file = gradio.File(label='File')
        with gradio.Column(scale=1.25):
            compressed_file = gradio.File(label='Compressed File')
            gradio.Button(value='Run').click(fn,
                                             inputs=[file],
                                             outputs=[compressed_file],
                                             api_name='api')
    gradio.Examples(examples='examples', inputs=[file])

api = gradio.mount_gradio_app(api, blocks, path='/gradio')
