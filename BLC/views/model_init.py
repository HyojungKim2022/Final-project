from django.conf import settings
from mmdet.apis import init_detector

cfg = 'models/hj/config_14.py'
ckpt = 'models/hj/epoch400/epoch_400.pth'

def init_model(cfg=cfg, ckpt=ckpt):
    model = getattr(settings, 'MY_MODEL', None)
    
    if model is None:
        model = init_detector(cfg, ckpt, device='cuda:0')
        li = ('65621', '50098', '30152', '45219', '30064', '30166', '50117', '50062', '30120', '20211', '10178', '45221', '10092', '30061', '10091', '30119', '25679', '30086', '50063', '15033', '45222', '65629', '65858', '30066', '50061', '20164', '10094', '90078', '30140', '15046', '45227', '30060', '15175', '10093', '65723', '90072', '10210', '30292', '10209', '45220', '35044', '30099', '30096', '65727', '65719', '65890', '90073', '10095', '20167', '30291')
        li = tuple(map(int, li))
        model.CLASSES = li

        setattr(settings, 'MY_MODEL', model)

    return model