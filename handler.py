import os
import json
import openai
import boto3

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
'''
Setting LINE
'''
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])

'''
Setting OpenAI
'''
openai.api_key = os.environ['OPENAI_API_KEY']



def webhook(event, context):
    # Parse msg from LINE conversation request
    print('event: ', event)
    msg = json.loads(event['body'])

    # Parse texts we type from msg
    user_id = msg['events'][0]['source']['userId']
    user_input = msg['events'][0]['message']['text']
    print('user_id: ', user_id)
    print('user_input:', user_input)

    comprehend = boto3.client('comprehend')
    try:
        source_language = comprehend.detect_dominant_language(Text=user_input)['Languages'][0]['LanguageCode']
    except IndexError:
        source_language = 'zh-TW'
    target_language = 'vi' if source_language == 'zh-TW' or source_language == 'zh' else 'zh-TW'

    # check if the conversation data exists
 
    prompt = []
    if target_language == 'vi':
        prompt.append({"role": "user", "content": "translate the following text to Vietnamese"})
    elif target_language == 'zh-TW':
        prompt.append({"role": "user", "content": "translate the following text to 繁體中文:"})

    prompt.append({"role": "user", "content": user_input})
    print('prompt: ', prompt)
    # GPT3
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    gpt3_response = response.choices[0]['message']['content']
    print('gpt3_response: ', gpt3_response)

    # handle webhook body
    try:
        line_bot_api.reply_message(
                msg['events'][0]['replyToken'],
                TextSendMessage(text=gpt3_response)
        )
    except:
        return {
            'statusCode': 502,
            'body': json.dumps("Invalid signature. Please check your channel access token/channel secret.")
        }
    return {
        "statusCode": 200,
        "body": json.dumps({"message": 'ok'})
    }