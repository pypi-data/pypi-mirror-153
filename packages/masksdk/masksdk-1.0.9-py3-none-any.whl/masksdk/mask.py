from PIL import Image, ImageFilter, ImageDraw

leak_height = 0.167


def blurring(image, boxes, degree):
    for b in boxes:
        class_name = b['class_name']
        if class_name == "face":
            bb = (b['x_min'], b['y_min'], b['x_max'], b['y_max'])
            cropped_image = image.crop(bb)
            mask = Image.new("L", cropped_image.size)
            draw = ImageDraw.Draw(mask)
            cxmin, cymin, cxmax, cymax = cropped_image.getbbox()
            cymin2 = min((cymin + max((cymax - cymin), 0) * leak_height), cymax)
            draw.ellipse((cxmin, cymin2, cxmax, cymax), fill=255)
            blurred = cropped_image.filter(ImageFilter.GaussianBlur(25 * float(degree)))
            cropped_image.paste(blurred, mask=mask)
            image.paste(cropped_image, bb)
        else:
            bb = (b['x_min'], b['y_min'], b['x_max'], b['y_max'])
            cropped_image = image.crop(bb)
            blurred_image = cropped_image.filter(ImageFilter.GaussianBlur(25 * float(degree)))
            image.paste(blurred_image, bb)
    return image


def pixelating(image, boxes, degree):
    for b in boxes:
        bb = (b['x_min'], b['y_min'], b['x_max'], b['y_max'])
        cropped_image = image.crop(bb)
        w, h = cropped_image.size
        small = cropped_image.resize((int(w / (float(degree) * w)), int(h / (float(degree) * h))), Image.BILINEAR)
        result = small.resize(cropped_image.size, Image.NEAREST)
        image.paste(result, bb)
    return image


def blackening(image, boxes, degree):
    for b in boxes:
        bb = (b['x_min'], b['y_min'], b['x_max'], b['y_max'])
        cropped = image.crop(bb)
        h, w = cropped.size
        black = Image.new(image.mode, (h, w), 'black')
        result = Image.blend(cropped, black, float(degree))
        cropped.paste(result)
        image.paste(cropped, bb)
    return image
