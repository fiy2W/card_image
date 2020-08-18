import os
import json
from PIL import Image

import torch
from torch.utils.data import Dataset
from torchvision import transforms

from .decoder import static_dict, setcode_dict, bincode_trans, setcode_trans


""" Basic dataset only generate image """
class BasicDataset(Dataset):
    def __init__(self, img_dir, transform=None):
        """ Need to be overloading

            data_dict:    a dict of data
            static_dict:  a dict of static information
            setcode_dict: a dict of setcode
            data_list:    a list of data to yield

        """
        self.img_dir = img_dir

        self.data_dict = self.load_datadict()
        self.static_dict = static_dict
        self.setcode_dict = setcode_dict

        self.data_list = list(self.data_dict.values())
        self.data_transform = transform
    
    def __len__(self):
        return len(self.data_list)
    
    def __getitem__(self, index):
        v = self.data_list[index]
        img_path = os.path.join(self.img_dir, '{}.png'.format(v['id']))
        img = Image.open(img_path)
        
        if self.data_transform is not None:
            img = self.data_transform(img)

        sample = {'image': img}
        return sample

    def load_datadict(self):
        """ Load the full data dict """
        with open(os.path.join(os.path.dirname(__file__), 'dict.json'), 'r') as f:
            data_dict = json.load(f)
            return data_dict
    
    def dict_search(self, dicts, func):
        """ Search some item from the input dicts """
        output = {}
        for k, v in dicts.items():
            if func(v):
                output[k] = v
        return output
    
    def show_item(self, id=None, idx=None):
        """ Output a sample's information in dict """
        if id is not None:
            try:
                v = self.data_dict[id].copy()
            except KeyError:
                print('Key {} is not in the dict.'.format(id))
                return {}
        elif idx is not None:
            try:
                v = self.data_list[idx].copy()
            except IndexError:
                print('Index {} is out of range {}.'.format(idx, self.__len__()))
                return {}
        else:
            return {}

        v['race'] = self.static_dict['race'][v['race']]
        v['attribute'] = self.static_dict['attribute'][v['attribute']]
        v['type'] = bincode_trans(v['type'], 'type')
        v['category'] = bincode_trans(v['category'], 'category')
        v['setcode'] = setcode_trans(v['setcode'])
        return v


""" Monster dataset generate image with label of race and attribute """
class MonsterDataset(BasicDataset):
    def __init__(self, img_dir, transform=None):
        self.img_dir = img_dir

        self.data_dict = self.dict_search(self.load_datadict(), self.search_monster)
        self.static_dict = static_dict
        self.setcode_dict = setcode_dict

        self.data_list = list(self.data_dict.values())
        self.data_transform = transform
    
    def __getitem__(self, index):
        v = self.data_list[index]
        img_path = os.path.join(self.img_dir, '{}.png'.format(v['id']))
        img = Image.open(img_path)
    
        if self.data_transform is not None:
            img = self.data_transform(img)

        sample = {'image': img, 'race': v['race'], 'attribute': v['attribute']}
        return sample
    
    def search_monster(self, v):
        typelist = bincode_trans(v['type'], 'type')
        # 去除没有种族和属性的衍生物
        if '怪兽' in typelist and v['race']>0 and v['attribute']>0:
            return True
        else:
            return False


data_transform = transforms.Compose([
    transforms.RandomResizedCrop(320, scale=(0.9, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
])
