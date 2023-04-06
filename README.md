# aws-translation-linebot

# Translation LINE bot with AWS

## System Overview

![](https://i.imgur.com/jYfHcxu.png)

## Getting Started

#### 事前準備

1. AWS Credentials

```L=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

2. LINE API

```L=
CHANNEL_ACCESS_TOKEN=
CHANNEL_SECRET=
```

## Development

1. Install **Serverless Framework**

```=
npm install -g serverless
```

2. Clone the project

```bash=
git clone https://github.com/Ianpengg/aws-translation-linebot.git
cd aws-translation-linebot
```

3. Create the conda environment

```=
conda create -n translation-bot python=3.8
conda activate translation-bot
pip install -r requirements
```

4. Set **AWS credentials**

```=
export AWS_ACCESS_KEY_ID=**********
export AWS_SECRET_ACCESS_KEY=***********
(For Windows)
set AWS_ACCESS_KEY_ID=**********
set AWS_SECRET_ACCESS_KEY=***********
```

5. Change the LINE credentials in `serverless.yml`

```=
CHANNEL_ACCESS_TOKEN= #your access token
CHANNEL_SECRET= #your channel secret
```

7. Install Plugin

```bash=
sls plugin install -n serverless-python-requirements
```

6. Deploy

```=
sls deploy
```

7. Set the webhook URL
   Open the LINE developer and enable the webhook -> paste the webhook generated in last step.
8. Try the translation bot in LINE

## Reference

1. [這次實作的 Github](https://github.com/Ianpengg/aws-translation-linebot)
2. [Chatgpt](https://openai.com/blog/chatgpt/)
3. [Serverless Framework](https://www.serverless.com/)
