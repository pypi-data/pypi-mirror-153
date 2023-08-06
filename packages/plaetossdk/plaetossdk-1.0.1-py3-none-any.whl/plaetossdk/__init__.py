import asyncio
import requests
import sys
import traceback


class Pipeline:

    def __init__(self, *steps):
        self.steps = steps

    def run(self, text):

        async def inner(line):
            result = {}
            for i, step in enumerate(self.steps):
                res = step(line)
                if step.__name__ == 'chunk':
                    chunks = []
                    for chunk in res['chunks']:
                        rs = {'original_text': chunk}
                        for s in self.steps[(i + 1):]:
                            r = s(chunk)
                            rs.update(r)
                        chunks.append(rs)
                    result.update({
                        **res,
                        'chunks': chunks,
                    })
                else:
                    result.update(res)
            return result

        async def main(lines):
            if isinstance(text, list):
                result = []
                for line in lines:
                    result.append(inner(line))
                return await asyncio.gather(*result)
            else:
                return await inner(text)

        try:
            return asyncio.run(main(text))

        except Exception as e:
            print('Error in pipeline:' + str(e))
            print('-' * 80)
            traceback.print_exc(file=sys.stdout)
            print('-' * 80)



class Client:

    def __init__(self, domain):
        self.domain = domain

    def chunk(self, text):
        try:
            url = f'https://chunker-service.default.{self.domain}/'
            if isinstance(text, list):
                url += 'predict_batch'
                payload = [{'text': line} for line in text]
            else:
                url += 'predict'
                payload = {'text': text}
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data
        except Exception as e:
            print(e)


    def emojify(self, text):
        try:
            url = f'https://emojify-service.default.{self.domain}/'
            if isinstance(text, list):
                url += 'predict_batch'
                payload = [{'doc': line} for line in text]
            else:
                url += 'predict'
                payload = {'doc': text}
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data
        except Exception as e:
            print(e)


    def emotion(self, text):
        try:
            url = f'https://emotion-service.default.{self.domain}/predict_batch'
            if isinstance(text, list):
                payload = text
            else:
                payload = [text]
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            if isinstance(text, list):
                return data
            if len(data) == 1:
                return data[0]
            return {'error': {'message': 'No results'}}
        except Exception as e:
            print(e)


    def pii(self, text):
        try:
            url = f'https://p-i-i-service.default.{self.domain}/'
            if isinstance(text, list):
                url += 'predict_batch'
                payload = [{'text': line} for line in text]
            else:
                url += 'predict'
                payload = {'text': text}
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data
        except Exception as e:
            print(e)


    def sentiment(self, text):
        try:
            url = f'https://sentiment-service.default.{self.domain}/'
            if isinstance(text, list):
                url += 'predict_batch'
                payload = [{'text': line} for line in text]
            else:
                url += 'predict'
                payload = {'text': text}
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data
        except Exception as e:
            print(e)


    def situation_solution(self, text):
        try:
            url = f'https://situation-solution-service.default.{self.domain}/'
            if isinstance(text, list):
                url += 'predict_batch'
                payload = [{'text': line} for line in text]
            else:
                url += 'predict'
                payload = {'text': text}
            res = requests.post(url, json=payload, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data
        except Exception as e:
            print(e)


    def topics(self, text):

        async def fetch(line):
            res = requests.post(url, json={'text': line}, headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            })
            data = res.json()
            return data

        async def main(lines):
            calls = []
            for line in lines:
                calls.append(fetch(line))
            return await asyncio.gather(*calls)

        try:
            url = f'https://topic-bento-service.default.{self.domain}/predict'
            if isinstance(text, list):
                data = asyncio.run(main(text))
            else:
                res = requests.post(url, json={'text': text}, headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                })
                data = res.json()
            return data
        except Exception as e:
            print(e)
