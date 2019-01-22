"""
Deploy rot and detect cloud functions and test them with this script.
It should solve the ROT number for the message text.
"""

import requests
from os import environ

HEADERS = {
    'X-Auth-Token': environ.get('TOKEN')
}

PROJECT = environ.get('PROJECT')

message = """
HFQQ rj Nxmrfjq.
Xtrj djfwx flt—sjajw rnsi mtb qtsl uwjhnxjqd—mfansl qnyyqj tw st rtsjd ns rd uzwxj,
fsi stymnsl ufwynhzqfw yt nsyjwjxy rj ts xmtwj, N ymtzlmy N btzqi xfnq fgtzy f qnyyqj fsi xjj ymj bfyjwd ufwy tk ymj btwqi.
"""

rot_url = f'https://europe-west1-{PROJECT}.cloudfunctions.net/rot'
detect_lang_url = f'https://europe-west1-{PROJECT}.cloudfunctions.net/detect-language'


def solve(message):
    for num in range(1, 26):
        rotted_text = requests.post(rot_url, json={'message': message, 'rot': num}, headers=HEADERS).json().get('data', '')
        translate = requests.post(detect_lang_url, json={'text': rotted_text}, headers=HEADERS).json()
        print(f'ROT-{num}', translate, rotted_text, '\n')
        if translate['confidence'] == 1 and translate['language'] == 'en':
            print(f'SOLVED with ROT {num}!')
            return rotted_text

solve(message)
