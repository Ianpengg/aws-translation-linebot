import os
import json
import boto3
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Initialize Line Bot SDK
line_bot_api = LineBotApi(os.environ['LINE_CHANNEL_ACCESS_TOKEN'])

def translate(event, context):

    msg = json.loads(event['body'])
    user_id = msg['events'][0]['source']['userId']
    user_input = msg['events'][0]['message']['text']
    print('user_id: ', user_id)
    print('user_input:', user_input)
    # Process each event in the webhook payload
    
    message = user_input
    print("msg", message)
    # Use AWS Translate and Comprehend to translate and detect the language of the message
    translate = boto3.client('translate')
    comprehend = boto3.client('comprehend')

    # Determine the source and target languages based on the detected language and the user's selected language
    print(comprehend.detect_dominant_language(Text=message)['Languages'])
    try:
        source_language = comprehend.detect_dominant_language(Text=message)['Languages'][0]['LanguageCode']
    except IndexError:
        source_language = 'zh-TW'
    target_language = 'en' if source_language == 'zh-TW' or source_language == 'zh' else 'zh-TW'

    # Perform the translation using AWS Translate
    translated_message = translate.translate_text(Text=message, SourceLanguageCode=source_language, TargetLanguageCode=target_language)['TranslatedText']

    # Construct the response message
    response_message = TextSendMessage(text=translated_message)

    # Send the translated message back to the user
    try:
        line_bot_api.reply_message(
                msg['events'][0]['replyToken'],
                response_message
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

