from PIL import Image
import glob

static_path = '/home/ec2-user/static/'
image_path = static_path + 'image/'


# path does not include extension, only id, it auto recognize extension after '.'
def image_ratio(path):
    path1 = glob.glob(path + '.*')
    assert path1, path
    image = Image.open(path1[0])
    return float(format(image.size[0] / image.size[1], '.6f'))
