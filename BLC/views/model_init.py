from django.conf import settings
from mmdet.apis import init_detector

cfg = 'models/hj/epoh14/config_14.py'
ckpt = 'models/hj/epoh14/epoch_14 (2).pth'

def init_model(cfg=cfg, ckpt=ckpt):
    model = getattr(settings, 'MY_MODEL', None)

    if model is None:
        model = init_detector(cfg, ckpt, device='cuda:0')

        setattr(settings, 'MY_MODEL', model)

    return model