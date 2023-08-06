from __future__ import division

import base64

import cv2
import numpy as np
import PIL


try:
    from turbojpeg import TurboJPEG
    jpeg = TurboJPEG()
except Exception:
    jpeg = None


def pil_to_cv2_interpolation(interpolation):
    if isinstance(interpolation, str):
        interpolation = interpolation.lower()
        if interpolation == 'nearest':
            cv_interpolation = cv2.INTER_NEAREST
        elif interpolation == 'bilinear':
            cv_interpolation = cv2.INTER_LINEAR
        elif interpolation == 'bicubic':
            cv_interpolation = cv2.INTER_CUBIC
        elif interpolation == 'lanczos':
            cv_interpolation = cv2.INTER_LANCZOS4
        else:
            raise ValueError(
                'Not valid Interpolation. '
                'Valid interpolation methods are '
                'nearest, bilinear, bicubic and lanczos.')
    else:
        if interpolation == PIL.Image.NEAREST:
            cv_interpolation = cv2.INTER_NEAREST
        elif interpolation == PIL.Image.BILINEAR:
            cv_interpolation = cv2.INTER_LINEAR
        elif interpolation == PIL.Image.BICUBIC:
            cv_interpolation = cv2.INTER_CUBIC
        elif interpolation == PIL.Image.LANCZOS:
            cv_interpolation = cv2.INTER_LANCZOS4
        else:
            raise ValueError(
                'Not valid Interpolation. '
                'Valid interpolation methods are '
                'PIL.Image.NEAREST, PIL.Image.BILINEAR, '
                'PIL.Image.BICUBIC and PIL.Image.LANCZOS.')
    return cv_interpolation


def decode_image_cv2(b64encoded):
    bin = b64encoded.split(",")[-1]
    bin = base64.b64decode(bin)
    bin = np.frombuffer(bin, np.uint8)
    img = cv2.imdecode(bin, cv2.IMREAD_COLOR)
    return img


def decode_image_turbojpeg(b64encoded):
    bin = b64encoded.split(",")[-1]
    bin = base64.b64decode(bin)
    img = jpeg.decode(bin)
    return img


def decode_image(b64encoded):
    if jpeg is not None:
        img = decode_image_turbojpeg(b64encoded)
    else:
        img = decode_image_cv2(b64encoded)
    return img


def encode_image_turbojpeg(img):
    bin = jpeg.encode(img)
    b64encoded = base64.b64encode(bin).decode('ascii')
    return b64encoded


def encode_image_cv2(img, quality=90):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    b64encoded = base64.b64encode(encimg).decode('ascii')
    return b64encoded


def encode_image(img):
    if jpeg is not None:
        img = encode_image_turbojpeg(img)
    else:
        img = encode_image_cv2(img)
    return img


def resize_keeping_aspect_ratio(img, width=None, height=None,
                                interpolation='bilinear'):
    if (width and height) or (width is None and height is None):
        raise ValueError('Only width or height should be specified.')
    if width == img.shape[1] and height == img.shape[0]:
        return img
    if width:
        height = width * img.shape[0] / img.shape[1]
    else:
        width = height * img.shape[1] / img.shape[0]
    height = int(height)
    width = int(width)
    cv_interpolation = pil_to_cv2_interpolation(interpolation)
    return cv2.resize(img, (width, height),
                      interpolation=cv_interpolation)


def resize_keeping_aspect_ratio_wrt_longside(img, length,
                                             interpolation='bilinear'):
    H, W = img.shape[:2]
    aspect = W / H
    cv_interpolation = pil_to_cv2_interpolation(interpolation)
    if H > W:
        width = length * aspect
        return cv2.resize(img, (int(width), int(length)),
                          interpolation=cv_interpolation)
    else:
        height = length / aspect
        return cv2.resize(img, (int(length), int(height)),
                          interpolation=cv_interpolation)


def squared_padding_image(img, length=None):
    H, W = img.shape[:2]
    if H > W:
        if length is not None:
            img = resize_keeping_aspect_ratio_wrt_longside(img, length)
        margin = img.shape[0] - img.shape[1]
        img = np.pad(img,
                     [(0, 0),
                      (margin // 2, margin - margin // 2),
                      (0, 0)], 'constant')
    else:
        if length is not None:
            img = resize_keeping_aspect_ratio_wrt_longside(img, length)
        margin = img.shape[1] - img.shape[0]
        img = np.pad(img,
                     [(margin // 2, margin - margin // 2),
                      (0, 0), (0, 0)], 'constant')
    return img


def masks_to_bboxes(mask):
    R, _, _ = mask.shape
    instance_index, ys, xs = np.nonzero(mask)
    bboxes = np.zeros((R, 4), dtype=np.float32)
    for i in range(R):
        ys_i = ys[instance_index == i]
        xs_i = xs[instance_index == i]
        if len(ys_i) == 0:
            continue
        y_min = ys_i.min()
        x_min = xs_i.min()
        y_max = ys_i.max() + 1
        x_max = xs_i.max() + 1
        bboxes[i] = np.array(
            [x_min, y_min, x_max, y_max],
            dtype=np.float32)
    return bboxes
