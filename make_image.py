import os
import sqlite3
import json
import math
from skimage.io import imread, imsave

from utils import mkdir
from decoder import *


def select_db(db_path):
    conn = sqlite3.connect(db_path)
    cu = conn.cursor()
    select_str = "select datas.id, datas.ot, datas.alias, datas.setcode, datas.type, \
                  datas.atk, datas.def, datas.level, datas.race, datas.attribute, datas.category, \
                  texts.name, texts.desc from datas inner join texts on datas.id=texts.id;"
    cu.execute(select_str)
    res = cu.fetchall()
    return res

    
def make_dict(data_raw):
    """
    ## Show the code with strings
    
    >>> bincode_trans(fill_code(bin(data_raw[4]), 27), 'type')
    >>> bincode_trans(fill_code(cate_decode(data_raw[10]), 32), 'category'))
    
    """
    card = {}
    card['id'] = data_raw[0]
    card['ot'] = data_raw[1]                                    # 1:ocg | 2:tcg | 3:ocg&tcg
    card['alias'] = data_raw[2]                                 # 0:None | others:id
    card['setcode'] = setcode_decode(data_raw[3])               # need to be decoded
    card['type'] = fill_code(bin(data_raw[4]), 27)              # need to be decoded
    card['atk'] = data_raw[5]                                   # attack
    card['def'] = data_raw[6]                                   # defence
    card['level'] = data_raw[7]                                 # level      0: spell,trap | others:monster
    card['race'] = log_decode(data_raw[8])                      # race       0: spell,trap | others:monster
    card['attribute'] = log_decode(data_raw[9])                 # attribute  0: spell,trap | others:monster
    card['category'] = fill_code(cate_decode(data_raw[10]), 32) # need to be decoded
    card['name'] = data_raw[11]                                 # name
    card['desc'] = data_raw[12]
    return card
    

if __name__ == '__main__':
    db_path = 'cards.cdb'
    pic_path = 'pics/'
    dict_path = 'dict.json'
    save_path = 'im/'
    mkdir(save_path)

    res = select_db(db_path)
    cards = {}

    for r in res:
        card = make_dict(r)
        cards[card['id']] = card
        im_card = imread(os.path.join(pic_path, '{}.jpg'.format(card['id'])))
        if card['type'][-25] == '1': # pendulum
            x = 28
            y = 104
            w = 344
            h = 256
        else:
            x = 50
            y = 107
            w = 302
            h = 302
        im = im_card[y:y+h, x:x+w, :]
        imsave(os.path.join(save_path, '{}.png'.format(card['id'])), im)

    with open(dict_path, 'w') as f:
        json.dump(cards, f, ensure_ascii=True)
