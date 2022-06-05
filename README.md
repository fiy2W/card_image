# YGO Card Image Dataset
A torch dataset for YGO card images.

## Install
- Copy `cards.cdb`, `strings.conf`, `pics/` from YGOPro.
- Generate card images.
    ```sh
    python make_image.py
    ```

## Usage
```python
from torchvision import transforms
from card_image.dataset import BasicDataset, MonsterDataset

data_transform = transforms.Compose([
    transforms.RandomResizedCrop(320, scale=(0.9, 1.0)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),
])

dataset = BasicDataset('card_image/im/', item_list=[
        'race', 'attribute', 'type', 'category', 'setcode',
    ], transform=data_transform)

monster_dataset = MonsterDataset('card_image/im/', item_list=[
        'race', 'attribute',
    ], transform=data_transform)
```