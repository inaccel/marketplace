import fastapi
import gradio
import io
import pandas
import subprocess

api = fastapi.FastAPI()


def fn(target, query, gap_open, gap_extend):
    return pandas.read_csv(io.BytesIO(
        subprocess.run([
            'ksw', '-q',
            str(gap_open), '-r',
            str(gap_extend), target.name, query.name
        ],
                       capture_output=True,
                       check=True).stdout),
                           sep='\t',
                           names=[
                               'Target Name', 'Target Start', 'Target End',
                               'Query Name', 'Query Start', 'Query End',
                               'Score', 'Score²', 'Target End²'
                           ])


with gradio.Blocks(analytics_enabled=False, title='Smith-Waterman') as blocks:
    gradio.Markdown(
        value='<h1 style="text-align: center; margin-bottom: 1rem">' +
        blocks.title + '</h1>')
    gradio.Markdown(
        value=
        'The **Smith-Waterman algorithm** performs *local sequence alignment*; that is, for determining similar regions between two strings (**Target**, **Query**) of *nucleic acid* sequences or *protein* sequences. Instead of looking at the entire sequence, the Smith-Waterman algorithm compares segments of all possible lengths and optimizes the similarity measure.'
    )
    with gradio.Row():
        with gradio.Column():
            with gradio.Row():
                with gradio.Column():
                    target = gradio.File(label='Target')
                with gradio.Column():
                    query = gradio.File(label='Query')
            gap_open = gradio.Slider(minimum=1,
                                     maximum=10,
                                     value=5,
                                     step=1,
                                     label='Opening')
            gap_extend = gradio.Slider(minimum=1,
                                       maximum=10,
                                       value=2,
                                       step=1,
                                       label='Extension')
        with gradio.Column(scale=1.25):
            output = gradio.Dataframe(headers=[
                'Target Name', 'Target Start', 'Target End', 'Query Name',
                'Query Start', 'Query End', 'Score', 'Score²', 'Target End²'
            ],
                                      label='Output',
                                      wrap=True)
            gradio.Button(value='Run').click(
                fn,
                inputs=[target, query, gap_open, gap_extend],
                outputs=[output],
                api_name='api')
    gradio.Examples(examples='examples',
                    inputs=[target, query, gap_open, gap_extend])

api = gradio.mount_gradio_app(api, blocks, path='/gradio')
