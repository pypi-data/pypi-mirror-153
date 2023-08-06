# Craft AI Python SDK

This Python SDK lets you interact with Craft AI MLOps Platform.

## Installation
This project relies on **Python 3.8+**. Once a supported version of Python is installed, you can install `craft-ai-sdk` from PyPI with:

```console
pip install craft-ai-sdk
```

## Basic usage
You can configure the SDK by instantiating the `CraftAiSdk` class in this way:

```python
from craft_ai_sdk import CraftAiSdk

ACCESS_TOKEN =  # your access token
ENVIRONMENT_URL =  # url to your environment

sdk = CraftAiSdk(token=ACCESS_TOKEN, environment_url=ENVIRONMENT_URL)
```
