from opencompass.multimodal.models.visualglm import (VisualGLMBasePostProcessor, VisualGLMBasePromptConstructor)

# dataloader settings
val_pipeline = [
    dict(type='mmpretrain.LoadImageFromFile'),
    dict(type='mmpretrain.ToPIL', to_rgb=True),
    dict(type='mmpretrain.torchvision/Resize',
         size=(224, 224),
         interpolation=3),
    dict(type='mmpretrain.torchvision/ToTensor'),
    dict(type='mmpretrain.torchvision/Normalize',
         mean=(0.48145466, 0.4578275, 0.40821073),
         std=(0.26862954, 0.26130258, 0.27577711)),
    dict(type='mmpretrain.PackInputs', algorithm_keys=['image_id'])
]


dataset = dict(type='mmpretrain.Flickr30kCaption',
               data_root='data/flickr30k',
               ann_file='annotations/dataset_flickr30k.json',
               data_prefix='images',
               split='val',
               pipeline=val_pipeline)

visualglm_flickr30k_dataloader = dict(batch_size=1,
                  num_workers=4,
                  dataset=dataset,
                  collate_fn=dict(type='pseudo_collate'),
                  sampler=dict(type='DefaultSampler', shuffle=False))

# model settings
visualglm_flickr30k_model = dict(
    type='visualglm',
    pretrained_path='/path/to/visualglm',  # or Huggingface repo id
    is_caption_task=True,
    prompt_constructor=dict(type=VisualGLMBasePromptConstructor, system_prompt='A photo of'),
    post_processor=dict(type=VisualGLMBasePostProcessor)
)

# evaluation settings
visualglm_flickr30k_evaluator = [
    dict(
        type='mmpretrain.COCOCaption',
        ann_file='data/flickr30k/annotations/flickr30k_val_gt.json',
    )  # noqa
]
