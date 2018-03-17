import logging

import jwt
from aiohttp import web
from aiohttp.web import json_response

from aiohttp_jwt import JWTMiddleware, check_permissions, match_any

logger = logging.getLogger(__name__)


secret = 'your secret'


async def foo_handler(request):
    return json_response({'status': 'OK'})


@check_permissions([
    'user:admin',
    'olehkuchuk',
], comparison=match_any)
async def protected_handler(request):
    payload = request.get('user', {})
    return json_response({
        'status': 'OK',
        'username': payload.get('username'),
    })


async def get_token(request):
    return jwt.encode({
        'username': 'olehkuchuk',
        'scopes': [
            'user:admin',
        ],
    }, secret)
    return None

app = web.Application(
    middlewares=[
        JWTMiddleware(
            secret=secret,
            request_property='user',
            token_getter=get_token,
            credentials_required=False,
            whitelist=[
                r'/(foo|bar)'
            ],
        ),
    ]
)

app.router.add_get('/foo', foo_handler)
app.router.add_get('/protected', protected_handler)

if __name__ == '__main__':
    web.run_app(app)
