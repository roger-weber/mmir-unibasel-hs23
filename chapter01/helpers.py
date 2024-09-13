import boto3
import json
import base64
import os
import time
import requests

session = boto3.Session(profile_name='default', region_name='us-east-1')
bedrock_client = session.client('bedrock', region_name='us-west-2')
bedrock_runtime_client = session.client('bedrock-runtime', region_name='us-west-2')

MODEL_ID = 'anthropic.claude-3-5-sonnet-20240620-v1:0'

def get_session():
    return session

def get_bedrock_client():
    return bedrock_client

def get_bedrock_runtime_client():
    return bedrock_runtime_client

def get_text2text_models():
    """
        return list of model for text to text with streaming; only return model ids
    """
    models = []
    for model in get_bedrock_client().list_foundation_models(byInferenceType='ON_DEMAND')['modelSummaries']:
        if not 'TEXT' in model['inputModalities']: continue
        if not 'TEXT' in model['outputModalities']: continue
        if not model.get('responseStreamingSupported', False): continue
        if model['modelName'] == 'Claude':
            model['modelName'] += ' ' + model['modelId'].split('-')[-1].replace(':', '.')
        models.append(model['modelId']+'/'+model['providerName']+' '+model['modelName'])
    return models


def enum_models(input_filter=['TEXT'], output_filter=['TEXT'], streaming=False):
    """
        enumerator for available models
    """
    for model in get_bedrock_client().list_foundation_models(byInferenceType='ON_DEMAND')['modelSummaries']:
        input_set, output_set = set(input_filter), set(output_filter)
        if input_set.intersection(set(model['inputModalities'])) != input_set or \
           output_set.intersection(set(model['outputModalities'])) != output_set or \
           streaming and not model.get('responseStreamingSupported', False):
            continue
        yield {
            'id': model['modelId'],
            'provider': model['providerName'],
            'name': model['modelName'],
            'typeText': str(model['inputModalities']) + " > " + str(model['outputModalities']),
            'streaming': model.get('responseStreamingSupported', False),
            'streamingText': model.get('responseStreamingSupported', False) and 'yes' or 'no'
        }

def anthropic_message_body(text, system=None, max_tokens=4096, image=None, temperature=None, top_p=None, top_k=None, history=None):
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": []
    }
    if system:
        body['system'] = system
    if max_tokens:
        body['max_tokens'] = max_tokens

    if history:
        roles = ['user', 'assistant']
        for i, message in enumerate(history):
            body['messages'].append({
                "role": roles[i % len(roles)],
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            })
    body['messages'].append(
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": text
                }
            ]
        }
    )
    if image:
        body['messages'][-1]['content'].append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": base64.b64encode(image).decode('utf-8')
            }
        })
    if temperature:
        body['temperature'] = temperature
    if top_p:
        body['top_p'] = top_p
    if top_k:
        body['top_k'] = top_k
    return json.dumps(body)

def invoke_model_claude(body):
    response = get_bedrock_runtime_client().invoke_model(
            body=body,
            modelId=MODEL_ID,
            accept="application/json",
            contentType="application/json",
        )
    return json.loads(response.get("body").read())['content'][0]['text']


class Prompts:
    def __init__(self, type):
        self.type = type
        self.prompts = {}

    @staticmethod
    def remove_prefix_suffix(text, prefix, suffix):
        return text.removeprefix(prefix).removesuffix(suffix)

    def get(self, name):
        self.update()
        return self.prompts.get(name, "")

    def set(self, name, description):
        self.prompts[name] = description
        with open(f'prompt_{self.type}_{name}.txt', 'w') as f:
            f.write(description)

    def update(self):
        self.prompts = {
            Prompts.remove_prefix_suffix(f, f'prompt_{self.type}_', '.txt'): open(f, 'r').read().strip() for f in os.listdir('.') if f.endswith('.txt') and f.startswith(f'prompt_{self.type}_')
        }

    def list(self):
        self.update()
        return list(self.prompts.keys())


image_prompts = Prompts('image')

def create_image_description(image, prompt):
    return invoke_model_claude(anthropic_message_body(
        image_prompts.get(prompt), 
        image=image
    ))

def chat_with_claude(text, history=None):
    return invoke_model_claude(anthropic_message_body(text, history=history))


class TranscribeJob:
    def __init__(self, job_name, media_uri, language_code='en-US'):
        self.job_name = job_name
        self.media_uri = media_uri
        self.language_code = language_code
        self.transcribe_client = session.client('transcribe')
        self.transcript_raw = None
        self.transcript = None

    def start(self):
        if self.get_status(): return
        self.transcribe_client.start_transcription_job(
            TranscriptionJobName=self.job_name,
            Media={'MediaFileUri': self.media_uri},
            MediaFormat='mp3',
            LanguageCode=self.language_code,
        )

    def get_status(self):
        try:
            response = self.transcribe_client.get_transcription_job(TranscriptionJobName=self.job_name)
            return response['TranscriptionJob']['TranscriptionJobStatus']
        except Exception:
            return None

    def is_finished(self):
        return self.get_status() == 'COMPLETED'

    def get_transcript(self):
        if not self.is_finished():
            return None
        if not self.transcript_raw:
            uri = self.transcribe_client.get_transcription_job(TranscriptionJobName=self.job_name)['TranscriptionJob']['Transcript']['TranscriptFileUri']
            data = requests.get(uri).text
            self.transcript_raw = json.loads(data)
            self.transcript = self.transcript_raw['results']['transcripts'][0]['transcript']
        return self.transcript


def s3_download(bucket, key):
    name = key.split('/')[-1]
    # return if file exists
    if os.path.exists(name): 
        return
    # otherwise create local file
    s3 = session.client('s3')
    with open(name, 'wb') as f:
        return s3.download_fileobj(bucket, key, f)

def s3_download_location(s3loc):
    bucket, key = s3loc.replace('s3://', '').split('/', 1)
    return s3_download(bucket, key)

def summarize_text(text):
    return invoke_model_claude(anthropic_message_body(
        "Summarize the following text:\n\n" + text
    ))