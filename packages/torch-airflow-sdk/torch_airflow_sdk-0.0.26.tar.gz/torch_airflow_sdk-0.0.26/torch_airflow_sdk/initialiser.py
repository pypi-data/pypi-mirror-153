import os

# setup these 3 env vars in your airflow environment. You can create api keys from torch ui's setting page.
torch_credentials = {
    'url': os.getenv('TORCH_CATALOG_URL', 'https://torch.acceldata.local:5443'),
    'access_key': os.getenv('TORCH_ACCESS_KEY', 'OY2VVIN2N6LJ'),
    'secret_key': os.getenv('TORCH_SECRET_KEY', 'da6bDBimQfXSMsyyhlPVJJfk7Zc2gs')
}