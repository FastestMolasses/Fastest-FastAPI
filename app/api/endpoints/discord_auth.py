import jwt
import json
import base64

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Assuming your templates are in a 'templates' directory

# JWT secret key
SECRET_KEY = "your_secret_key_here"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def createOAuthSession():
    # Your logic for creating an OAuth session
    pass

def generateKey():
    # Your logic for generating a key
    pass

def removeStripeCookies():
    # Your logic to remove Stripe cookies
    pass

def userHasDiscordAuthToken(token: str = Depends(oauth2_scheme)) -> bool:
    # Decode JWT token and verify user has Discord auth token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return bool(payload.get("discord_auth"))
    except:
        return False

@app.get("/signin")
async def signin(request: Request, token: str = Depends(oauth2_scheme)):
    if userHasDiscordAuthToken(token):
        # Redirect to the license page
        return RedirectResponse(url_for('auth.license'))

    oauth = createOAuthSession()
    state = {
        'nonce': generateKey(),
    }
    nextUrl = request.query_params.get('next')
    if nextUrl:
        state.update({'redirect': nextUrl})

    state = saveAsState(state)
    loginUrl, state = oauth.authorization_url(
        Config.DISCORD_AUTHORIZE_URL, state=state)
    response = templates.TemplateResponse('auth/authWithDiscord.html', {
        "request": request,
        "title": 'Waffler Sign In',
        "loginUrl": loginUrl
    })
    response.set_cookie(key=Cookies.DISCORD_STATE, value=state)

    removeStripeCookies()
    return response

@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(url=request.query_params.get('next', '/'))
    # Your logic to remove all cookies, for example:
    response.delete_cookie(key="your_cookie_name")
    return response

@app.get("/oauth_callback")
def discordOAuthCallback(request: Request):
    state = request.query_params.get('state', '')
    if not state or state != request.cookies.get(Cookies.DISCORD_STATE):
        return RedirectResponse('/')

    oauth = createOAuthSession()
    try:
        token = oauth.fetch_token(
            Config.DISCORD_TOKEN_URL,
            client_secret=Config.DISCORD_CLIENT_SECRET,
            authorization_response=request.url,
        )
    except Exception:
        return RedirectResponse('/')

    jwt_token = jwt.encode({"discord_auth": token}, SECRET_KEY, algorithm="HS256")

    state_dict = getState(request)
    if state_dict.get('redirect'):
        params = state_dict.get('params', {})
        redir = state_dict.get('redirect')
        if params:
            redir += '?' + urlencode(params)

        response = RedirectResponse(redir)
    else:
        # Go to the user profile on default
        response = RedirectResponse(url_for('userDashboard.userProfile'))

    response.set_cookie(key=Cookies.DISCORD_TOKEN, value=jwt_token)
    return response

def saveAsState(state: dict) -> str:
    state = json.dumps(state)
    return base64.b64encode(state.encode()).decode()

def getState(request: Request) -> dict:
    state = request.cookies.get(Cookies.DISCORD_STATE, '')
    if not state:
        return {}

    state = base64.b64decode(state).decode()
    return json.loads(state)
