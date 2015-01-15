#! /usr/bin/env python3.4
# -*- coding: utf-8 -*-
import sys
import json
import logging
import random
import urllib.request


# logger の初期化
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '[%(asctime)s][%(name)s] %(levelname)s %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class DocomoZatsudanClient(object):
    '''Docomo 雑談 API と雑談する Client
    概要は以下
    https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_docs_id=17
    '''

    # BASE URL
    BASEURL = 'https://api.apigw.smt.docomo.ne.jp/dialogue/v1/dialogue'

    # API KEY
    APIKEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # 雑談相手の特徴
    # とりあえず API コンソールまま
    nickname = '光'
    nickname_y = 'ヒカリ'
    sex = '女'
    bloodtype = 'B'
    birthdateY = '1997'
    birthdateM = '5'
    birthdateD = '30'
    age = '16'
    constellations = '双子座'
    place = '東京'

    # 通常の会話 (dialog) かしりとり(srtr) か
    mode = 'dialog'

    # API に渡す引数
    parameters = ('nickname', 'nickname_y', 'sex', 'bloodtype', 'birthdateY',
                  'birthdateM', 'birthdateD', 'age', 'constellations', 'place',
                  'mode')

    # 引き続き会話を続ける場合同じ値を指定する
    context = None

    def __init__(self, *args, **kwargs):
        '''会話パラメーターを初期化し、コンテキストを決定する'''
        for key in self.parameters:
            value = kwargs.get(key, getattr(self, key))
            setattr(self, key, value)

        # context が未指定の場合、初期化して設定する
        self.context = kwargs.get('context', self._get_new_context())

    @staticmethod
    def _get_new_context():
        '''コンテキスト文字列を返す ([0-9a-z] 64文字)'''
        _seq = [chr(x) for x in list(range(48, 58)) + list(range(97, 123))]
        return ''.join([random.choice(_seq) for x in range(64)])

    def talk(self, message, context=None):
        '''雑談 API と会話する'''
        context = context or self.context
        data = json.dumps(self._build_parameter(message, context))
        req = urllib.request.Request(self._get_url(), data.encode('utf-8'),
                                     {'Content-Type': 'application/json'})
        response = urllib.request.urlopen(req)
        return json.loads(response.read().decode('utf-8'))['utt']

    def _build_parameter(self, message, context):
        '''パラメーターを構築して辞書を返す'''
        assert len(message) < 256, ('Please specify message '
                                    'less than 256 letters.')

        param = {'utt': message, 'context': context}
        for key in self.parameters:
            param[key] = getattr(self, key)
        return param

    def _get_url(self):
        '''API のエンドポイント URL を返す'''
        return self.BASEURL + '?APIKEY=' + self.APIKEY


class DocomoSrtrClient(DocomoZatsudanClient):
    '''しりとりクライアント'''
    mode = 'srtr'
