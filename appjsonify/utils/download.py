import os
import zipfile

import requests
from tqdm import tqdm

from .error import DownloadFailureError

def _download(config: dict):
    output_path: str = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        config["output_path"]
    )
    print(f"    Downloading a file from {config['url']} to {output_path}...")
    response = requests.get(config["url"], stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        with open(output_path, "wb") as f, tqdm(
            desc=output_path,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(chunk_size=1024):
                size = f.write(data)
                bar.update(size)
        print("\tDownload complete.")
        
        if config["is_zip"]:
            # Unzip the downloaded file
            with zipfile.ZipFile(output_path, "r") as zip_ref:
                unzipped_path: str = '/'.join(output_path.split('/')[:-1])
                zip_ref.extractall(unzipped_path)
            print("\tUnzipped weights.")
            
            # Delete the original downloaded file
            os.remove(output_path)
            print("\tDeleted original downloaded file.")
    else:
        raise DownloadFailureError("\tFailed to download file from {}.".format(config['url']))


def download_individual_file(
    model_type: str,
    file_type: str
):
    """Download an individual file."""
    configs = {
        "tablebank": {
            "base": {
                "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
                "output_path" : "weights/tablebank/configs/Base-RCNN-FPN.yaml",
                "is_zip": False
            },
            "config": {
                "url": "https://layoutlm.blob.core.windows.net/tablebank/model_zoo/detection/All_X152/All_X152.yaml?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
                "output_path": "weights/tablebank/X152/All_X152.yaml",
                "is_zip": False
            },
            "weight": {
                "url": "https://layoutlm.blob.core.windows.net/tablebank/model_zoo/detection/All_X152/model_final.pth?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
                "output_path": "weights/tablebank/X152/model_final.pth",
                "is_zip": False
            },
        },
        "publaynet": {
            "base": {
                "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
                "output_path" : "weights/publaynet/X101/Base-RCNN-FPN.yaml",
                "is_zip": False
            },
            "config": {
                "url": "https://raw.githubusercontent.com/hpanwar08/detectron2/master/configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml",
                "output_path": "weights/publaynet/X101/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml",
                "is_zip": False
            },
            "weight": {
                "url": "https://www.dropbox.com/sh/1098ym6vhad4zi6/AAD8Y-SVN6EbfAWEDYuZHG8xa/model_final_trimmed.pth?dl=1",
                "output_path": "weights/publaynet/X101/model_final_trimmed.pth",
                "is_zip": False
            }
        },
        "docbank": {
            "base": {
                "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
                "output_path" : "weights/configs/Base-RCNN-FPN.yaml",
                "is_zip": False
            },
            "config": {
                "url": "https://layoutlm.blob.core.windows.net/docbank/model_zoo/X101.zip?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
                "output_path": "weights/docbank/X101.zip",
                "is_zip": True
            },
            "weight": {
                "url": "https://layoutlm.blob.core.windows.net/docbank/model_zoo/X101.zip?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
                "output_path": "weights/docbank/X101.zip",
                "is_zip": True
            },
        }
    }
    config = configs[model_type][file_type]
    _download(config)
    

def download():
    download_configs = [
        # Common
        {
            "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
            "output_path" : "weights/tablebank/configs/Base-RCNN-FPN.yaml",
            "is_zip": False
        },
        {
            "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
            "output_path" : "weights/configs/Base-RCNN-FPN.yaml",
            "is_zip": False
        },
        {
            "url": "https://raw.githubusercontent.com/facebookresearch/detectron2/cbbc1ce26473cb2a5cc8f58e8ada9ae14cb41052/configs/Base-RCNN-FPN.yaml",
            "output_path" : "weights/publaynet/X101/Base-RCNN-FPN.yaml",
            "is_zip": False
        },
        # TableBank
        {
            "url": "https://layoutlm.blob.core.windows.net/tablebank/model_zoo/detection/All_X152/All_X152.yaml?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
            "output_path": "weights/tablebank/X152/All_X152.yaml",
            "is_zip": False
        },
        {
            "url": "https://layoutlm.blob.core.windows.net/tablebank/model_zoo/detection/All_X152/model_final.pth?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
            "output_path": "weights/tablebank/X152/model_final.pth",
            "is_zip": False
        },
        # DocBank -> need to unzip
        {
            "url": "https://layoutlm.blob.core.windows.net/docbank/model_zoo/X101.zip?sv=2022-11-02&ss=b&srt=o&sp=r&se=2033-06-08T16:48:15Z&st=2023-06-08T08:48:15Z&spr=https&sig=a9VXrihTzbWyVfaIDlIT1Z0FoR1073VB0RLQUMuudD4%3D",
            "output_path": "weights/docbank/X101.zip",
            "is_zip": True
        },
        # PublayNet
        {
            "url": "https://www.dropbox.com/sh/1098ym6vhad4zi6/AAD8Y-SVN6EbfAWEDYuZHG8xa/model_final_trimmed.pth?dl=1",
            "output_path": "weights/publaynet/X101/model_final_trimmed.pth",
            "is_zip": False
        },
        {
            "url": "https://raw.githubusercontent.com/hpanwar08/detectron2/master/configs/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml",
            "output_path": "weights/publaynet/X101/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml",
            "is_zip": False
        }
    ]

    for config in download_configs:
        _download(config)

