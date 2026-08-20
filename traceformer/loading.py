"""Model/tokenizer loading, shared by every study script.

Previously each study in studies/ duplicated this boilerplate (and
disagreed on it -- some scripts used the slow GPT2Tokenizer, others
GPT2TokenizerFast for offset-mapping support, and only some set
HF_HUB_OFFLINE). This settles on the fast tokenizer everywhere, since
it's a strict superset of what the slow one offers.
"""

import os

from transformers import GPT2LMHeadModel, GPT2TokenizerFast


def load_gpt2(offline: bool = True):
    """Load GPT-2 + its tokenizer, ready for inference (model.eval()'d).

    offline: try loading with HF_HUB_OFFLINE=1 first, so a cached model
    loads without touching the network. If the weights aren't cached
    locally, this prints a notice and retries with the network allowed,
    so the first run downloads them instead of failing outright. Set
    False to skip the offline attempt and always allow network access.
    """
    if offline:
        os.environ["HF_HUB_OFFLINE"] = "1"
        try:
            tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
            model = GPT2LMHeadModel.from_pretrained("gpt2")
        except OSError:
            print("gpt2 not found in local cache; downloading from Hugging Face Hub...")
            os.environ.pop("HF_HUB_OFFLINE", None)
            tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
            model = GPT2LMHeadModel.from_pretrained("gpt2")
    else:
        tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
        model = GPT2LMHeadModel.from_pretrained("gpt2")

    model.eval()
    return tokenizer, model
