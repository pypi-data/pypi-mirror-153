


# Brikeda Client

Client Proxy to call AI Services on Brikeda, and Classes to support hardware on Raspberry Pi such as waveshare motor controller

## Instructions

1. Install:

```
pip install brikeda_client
```

2. Generate an Brikeda object and call some methods:

```python
from brikeda_client.brikeda import Brikeda

# initialize Brikeda Object with personal key retrieved at brikeda.com/aipanel
brik=Brikeda("4b6871e0d9d84de2926df29483a9aab9")
# send a message. any string will do. but if is a valid hex color it will display it
brik.SyncMessages("#ebde34")
# get a sentiment analysis of a sentence:postive, negative ratings
x = brik.Sentiment('this is exciting')
print(x)

```

