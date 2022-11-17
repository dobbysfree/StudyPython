import requests
from PIL import Image
import hashlib

url = 'https://byline.network/wp-content/uploads/2018/05/cat.png'
r = requests.get(url, stream=True).raw

img = Image.open(r)
img.show()
img.save('src.png')

print(img.get_format_mimetype)

BUF_SIZE = 1024
with open('../ch3/src.png', 'rb') as sf, open('../ch3/dst.png', 'wb') as df:
    while True:
        data = sf.read(BUF_SIZE)
        if not data:
            break
        df.write(data)

sha_src = hashlib.sha256()
sha_dst = hashlib.sha256()

with open('../ch3/src.png', 'rb') as sf, open('../ch3/dst.png', 'rb') as df:
    sha_src.update(sf.read())
    sha_dst.update(df.read())

print("src.png's hash : {}".format(sha_src.hexdigest()))
print("dsc.png's hash : {}".format(sha_dst.hexdigest()))