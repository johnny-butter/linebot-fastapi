import re
import json

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent

from fastapi import APIRouter, HTTPException, Header, Request

from config import settings
from models import db_session, Keywords
from services import response

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
webhook_parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

router = APIRouter()


@router.post('/callback')
async def bot_callback(
    request: Request,
    x_line_signature: str = Header(None)
):

    body = await request.body()

    try:
        events = webhook_parser.parse(body.decode('utf-8'), x_line_signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature error")
    except LineBotApiError:
        raise HTTPException(status_code=400, detail="Line bot api error")

    keywords_with_cls = db_session().query(Keywords.keyword, Keywords.response_cls).all()

    for event in events:
        if not isinstance(event, MessageEvent):
            return

        if json.loads(str(event))['message']['type'] == 'text':
            for keyword, resp_cls_name in keywords_with_cls:
                if re.search(keyword + '$', event.message.text):
                    if not hasattr(response, resp_cls_name):
                        raise ValueError(f'No {resp_cls_name} method')

                    resp_cls = getattr(response, resp_cls_name)

                    line_bot_api.reply_message(
                        event.reply_token,
                        resp_cls(line_event_message=event.message.text).response()
                    )

                    break

        elif json.loads(str(event))['message']['type'] == 'sticker':
            line_bot_api.reply_message(
                event.reply_token,
                response.RandomLineSticker().response()
            )

    return {'status': 'success'}
