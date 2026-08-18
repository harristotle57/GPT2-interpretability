"""
A first attempt to see if GPT2 is capable of aligning strings into columns.
"""

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

import os
os.environ["HF_HUB_OFFLINE"] = "1"

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

# --- Few-shot column alignment test ---
# Base GPT-2 isn't instruction-tuned, so asking it to "please align these
# columns" doesn't work. Instead, show one worked example so it can pattern
# match the continuation. Greedy decoding (do_sample=False) is used since
# this is a precision task, not a creative one.

alignment_prompt = """
Zhorerfvek | | Quintal |  | 1804
Bramnos |    | Vexley |   | 1805
Trilqaue |   | Omenn |    | 1806
Yandrik |    | Farrow |   | 1807
Corvasi |    | Thredmon | | 1808
Nalpfdshet | | Grissu |   | 1809
Ovrebcnth |  | Caskil |   | 1810
Drenmaau |   | Pisk |     | 1811
Krahel |     | Dnvash |   | 1812
Melgrast |   | Voskiel |  | 1813
Qutheba |    | Larnoux |  | 1814
Frendulac |  | Ytrim |    | 1815
Vhvnaarniss || Toblerek | | 1816
Sondrayel |  | Prixnal |  | 1817
Wexune |     | Gmtal |    | 1818
Halquiver |  | Naemrosk | | 1819
Iskavred |   | Doddltiam || 1820
Ephral |     | Wistock |  | 1821
"""

alignment_inputs = tokenizer(alignment_prompt, return_tensors="pt")
prompt_len = alignment_inputs["input_ids"].shape[1]
alignment_output_ids = model.generate(**alignment_inputs,
                                      max_new_tokens=60,
                                      min_new_tokens=10,
                                      do_sample=False,
                                      repetition_penalty=1.01)
output_string = tokenizer.decode(alignment_output_ids[0][prompt_len:], skip_special_tokens=True)
print(output_string)

notes = """ Notes on this work
It has been difficult to find a spacing pattern than GPT2 is capable of repeating. I tried with spaces aligning the first characters of each column. GPT2 also struggled with that pattern for a few reasons. I initially had real names, which didn't work because GPT2 just continued with basically an encyclopedia entry based on the last name. I had Claude generate some fake names for me that it couldn't pick up any meaningful connection to. I noticed along the way that it was correctly incrementing the year counter, which has persisted in every iteration I've observed. In order to help it accomplish the task at hand, I added the pipes to the beginning of each column, which seems to help it understand the pattern a bit better. However, it still struggles to count correctly. I added a set of pipes at the end of each column and that did seem to improve things a bitmore, but it still can't count well. One resource indicated that it may be a tokenization issue, where different numbers of spaces might be tokenized in a way that compresses them and obscures things from the model. However, a quick test indicated that isn't the case. Perhaps it would be meaningful to look into the tokenization of the full string, perhaps it is following that pattern, but it isn't so obvious to me because I don't see how each name gets tokenized. In any case, this question is probably not going to lead to the same destination as the paper. We could still study why GPT2 is struggling with this task, or we can look into how it knows how to count the years. It's unclear to me what is most fruitful.
"""
