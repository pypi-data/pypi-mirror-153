import jinja2
import os
import io
import base64
from typing import Optional
from chalice import Response, Chalice
from magic import Magic
from chalice_http_toolkit.response_with_binary import ResponseWithBinary
import json
from PIL import Image

class ContentManager:
    """
    Creates a ContentManager instance which allows rendering templates, returning static content
    and dynamic assets plus more. Generally after a ContentManager is called, set_static_handler_prefix()
    should be called directlty after to setup your static() handler in Jinja templates.

    :param templates_dir: Base path for templates
    :param static_dir: Base path for static content
    :param app: Chalice app
    :param magic: Optional python-magic instance, often required given Lambda hosts dont have libmagic installed.
    :returns: ContentManager instance
    """
    def __init__(self, templates_dir:str, static_dir:str, app:Chalice, magic:Optional[Magic]=None):
        self.templates_dir = templates_dir
        self.static_dir = static_dir
        self.__allowed_static_files = os.listdir(static_dir)
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
        self.__magic = magic if magic else Magic(mime=True)
        self.__app = app

    def set_static_handler_prefix(self, path:str):
        """
        Defines a function static() to allow dynamic resolution of static content
        in templates. The path argument should correlate with a Chalice endpoint to fetch
        the static content.

        :param path: Path to match chalice endpoint in which static() calls will match in templates.
        :returns: None
        """
        self.env.globals.update({'static': lambda x: f'{path}/{x}'})

    def render_template(self, filename:str, **kwargs) -> str:
        """
        Renders a template using the existing Jinja2 environment.

        :param filename: Path to template
        :param kwargs: Additional kwargs to be passed into template render
        :returns: Rendered template as a string
        """
        return self.env.get_template(filename).render(kwargs)

    def convert_by_accepts(self, img:bytes, accepts:str, default='WEBP') -> bytes:
        """
        Converts an images type based on the accepts format (ie image/jpeg) using Pillow.
        If default=None, will throw an exception if no conversion found.

        :param img: Bytes of image
        :param accepts: Mimetype format, current supports: image/jpeg, image/jpg, image/webp, image/png, image/gif
        :param default: Default format if cant convert, prevents an exception being thrown if cant convert.
        :returns: Converted image
        :raises: Exception if cant find matching type to convert to
        """
        accepts2pil = {'image/jpeg': 'JPEG',
                       'image/jpg': 'JPEG',
                       'image/webp': 'WEBP',
                       'image/png': 'PNG',
                       'image/gif': 'GIF'}
        new_format = default
        for t in accepts.split(','):
            if t in accepts2pil:
                new_format = accepts2pil[t]
                break
        else:
            if default is None:
                raise Exception('Couldnt match accepts with supported formats: %s' % accepts)
        image = Image.open(io.BytesIO(img))
        with io.BytesIO() as output:
            image.save(output, format=new_format)
            converted = output.getvalue()
        return converted

    def asset(self, body:bytes, status_code:int=200, headers:Optional[dict]=None) -> ResponseWithBinary:
        """
        Useful for returning dynamic static content such as images loaded from a database.

        :param body: Bytes representing content to return
        :param status_code: Status code to return content with
        :param headers: Additional headers to return
        :returns: Chalice Response object
        """
        h = {"Access-Control-Allow-Origin": "*"}
        if headers:
            h = {**h, **headers}
        h["Content-Type"] = self.__magic.from_buffer(body)
        r = ResponseWithBinary(body=body, status_code=status_code, headers=h)
        r.isBase64Encoded = True
        return r

    def static(self, filename:str, status_code:int=200, headers:Optional[dict]=None) -> ResponseWithBinary:
        """
        Useful for returning static content in the configured static directory.

        :param filename: Path relative from static_dir to content
        :param status_code: Status code to return content with
        :param headers: Additional headers to return
        :returns: Chalice Response object
        """
        if filename not in self.__allowed_static_files:
            print('Ignored %s' % filename)
            return Response(body='', status_code=404)

        h = {"Access-Control-Allow-Origin": "*"}
        if headers:
            h = {**h, **headers}
        with open(os.path.join(self.static_dir, filename), 'rb') as f:
            body = f.read()
        if filename.endswith('.css'):
            content_type = 'text/css'
        elif filename.endswith('.js'):
            content_type = 'text/javascript'
        else:
            content_type = self.__magic.from_buffer(body)

        isBase64Encoded = False
        if content_type.startswith('image/'):
            if self.__app.current_request:
                accepts = self.__app.current_request.headers.get('accept', '')
                if accepts:
                    body = self.convert_by_accepts(body, accepts)
                    content_type = self.__magic.from_buffer(body)
            isBase64Encoded = True
        h["Content-Type"] = content_type
        r = ResponseWithBinary(body=body, status_code=status_code, headers=h)
        r.isBase64Encoded = isBase64Encoded
        return r

    def html(self, body:str, status_code:int=200, headers:Optional[dict]=None) -> Response:
        """
        Useful for returning html content that has been rendered already using render_template().

        :param body: String containing rendered template
        :param status_code: Status code to return content with
        :param headers: Additional headers to return
        :returns: Chalice Response object
        """
        h = {"Content-Type": "text/html", "Access-Control-Allow-Origin": "*"}
        if headers:
            h = {**h, **headers}
        return Response(body=body, status_code=status_code, headers=h)

    def json(self, body:str, status_code:int=200, headers:Optional[dict]=None) -> Response:
        """
        Useful for returning json content.

        :param body: String containing json
        :param status_code: Status code to return content with
        :param headers: Additional headers to return
        :returns: Chalice Response object
        """
        h = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
        if headers:
            h = {**h, **headers}
        return Response(body=json.dumps(body), status_code=status_code, headers=h)

    def redirect(self, url:str) -> Response:
        """
        Generates a 301 redirect Response.

        :param url: URL to redirect to
        :returns: Chalice Response object
        """
        return Response(status_code=301,
                        body='',
                        headers={'Location': url})