# Inkit
This is an Inkit SDK.

### Installing:

`pip install inkit`

### Help:
Check docstrings by typing:
```
import inkit

help(inkit.Render.create)
```

### Usage Examples:
```
import inkit
from inkit.exceptions import InkitResponseException


inkit.api_token = 'xxxxxtokenxxxxx'


# Renders Create

try:
    resp = inkit.Render.create(
        html='<html>My awesome HTML</html>',
        width=6.5,
        height=11.5,
        unit="in"
    )
except InkitResponseException as e:
    logger.exception(
        'Exception while creating render',
        message=e.message,
        data=e.response.data
    )

render_data = resp.data
logger.info(f'Successfully created render {render_data.id}', data=render_data)


# Renders Retrieve

resp = inkit.Render.get('rend_12345')
render_data = resp.data


# Renders List

resp = inkit.Render.list(
    page_size=2,
    page=2,
    sort='-created_at',
    search='test',
    data_id='rend_123,rend_1234,rend_id_12345'
)
renders = resp.data.items


# Renders get PDF

resp = inkit.Render.get_pdf('rend_12345')
content = resp.content


# Renders get DOCX

resp = inkit.Render.get_docx('rend_12345')
content = resp.content


# Renders get HTML

resp = inkit.Render.get_html('rend_12345')
html = resp.text


# Renders Delete

resp = inkit.Render.delete('rend_12345')
```
