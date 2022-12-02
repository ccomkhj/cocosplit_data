
## ※※※ Base code ※※※
https://github.com/akarazniewicz/cocosplit / akarazniewicz 
(coco, train, test split)

- In the existing code, fix error (confusion between valiation and test dataset) and update no test mode (only split into train and validation dataset).


## init enviornment
pip install -r requirements.txt


## How to use?
```bash
python cocosplit_train_test_valid.py \\  
--annotations {annotationsFile, only Json} \\  
--train_ratio {own train_ratio} \\  
--valid_ratio {own valid_ratio} \\  
--test_ratio {own test_ratio} \\  
--trainJson_name {save fileName, Has a default} \\  
--validJson_name {save fileName, Has a default} \\  
--testJson_name {save fileName, Has a default} \\  
--save_path {choose utput path, Has a default} \\  
--image_path {choose coco dataset image files path, Has a default} \\  
--os {choose your computer operating system, default linux}  
--no_test
```

## example
```bash
python cocosplit_train_test_valid.py \\  
--annotations ./target.json \\  // input your target json file path  
--train_ratio 0.8 \\  
--valid_ratio 0.1 \\  
--test_ratio 0.1 \\  
--trainJson_name train.json \\  
--validJson_name valid.json \\  
--testJson_name test.json \\  
--save_path /output \\  
--image_path ./cocoDataset/image \\  
--os window  
```

```bash
python cocosplit_train_test_valid.py \\  
--annotations ./target.json \\  // input your target json file path  
--train_ratio 0.9 \\  
--valid_ratio 0.1 \\  
--trainJson_name train.json \\  
--validJson_name valid.json \\  
--testJson_name test.json \\  
--save_path /output \\  
--image_path ./cocoDataset/image \\  
--os window  
--no_test
```


## what is 'cocosplit_train_test_valid.py' and 'cocosplit_train_test_valid_fileVer.py'
'cocosplit_train_test_valid.py' version is just split json file to train, test, valid file  
'cocosplit_train_test_valid_fileVer.py' version is split json file and copy real files to json path

## Option information
```bash
python cocosplit_train_test_valid.py -h
```
