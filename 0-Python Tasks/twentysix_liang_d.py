from PIL import Image
def twentysix():
    image = Image.open(input('Image filename: ')) # This may not work, I can't get PIL to work
    print(image.size())

twentysix()
exit()