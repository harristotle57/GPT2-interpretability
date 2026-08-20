"""
A first attempt to see if GPT2 is capable of aligning strings into columns.
"""

notes = ""

import torch

from traceformer.loading import load_gpt2
from _wrapping import wrap_to_width, check_wrap_width

tokenizer, model = load_gpt2()

# --- Few-shot column alignment test ---
# Base GPT-2 isn't instruction-tuned, so asking it to "please align these
# columns" doesn't work. Instead, we will show one worked example so it can pattern
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

notes += """ Notes after column alignment test.
It has been difficult to find a spacing pattern than GPT2 is capable of repeating. I tried with spaces aligning the first characters of each column. GPT2 also struggled with that pattern for a few reasons. I initially had real names, which didn't work because GPT2 just continued with basically an encyclopedia entry based on the last name. I had Claude generate some fake names for me that it couldn't pick up any meaningful connection to. I noticed along the way that it was correctly incrementing the year counter, which has persisted in every iteration I've observed. In order to help it accomplish the task at hand, I added the pipes to the beginning of each column, which seems to help it understand the pattern a bit better. However, it still struggles to count correctly. I added a set of pipes at the end of each column and that did seem to improve things a bitmore, but it still can't count well. One resource indicated that it may be a tokenization issue, where different numbers of spaces might be tokenized in a way that compresses them and obscures things from the model. However, a quick test indicated that isn't the case. Perhaps it would be meaningful to look into the tokenization of the full string, perhaps it is following that pattern, but it isn't so obvious to me because I don't see how each name gets tokenized. In any case, this question is probably not going to lead to the same destination as the paper. We could still study why GPT2 is struggling with this task, or we can look into how it knows how to count the years.

Next we will try to recreate the paper's query, and see if GPT2 can estimate line length accurately enough to say something.
"""

ipsum_text = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam feugiat ipsum tortor, ut varius lorem auctor ut. Ut venenatis purus sapien, laoreet dictum purus maximus nec. Suspendisse aliquet velit arcu, laoreet cursus odio euismod eu. Maecenas mattis, tortor nec lacinia sagittis, lorem lectus fringilla metus, sed molestie ex tellus eget erat. Nam venenatis tortor urna, in elementum sem consequat vel. Maecenas aliquet purus arcu, nec congue enim malesuada eu. Donec eu maximus elit. Nullam lobortis sodales ex quis condimentum."""

other_text = """It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings or views of such a man may be on his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding families, that he is considered as the rightful property of some one or other of their daughters.
"""

alignment_inputs = tokenizer(wrap_to_width(other_text, 60), return_tensors="pt")
prompt_len = alignment_inputs["input_ids"].shape[1]
alignment_output_ids = model.generate(**alignment_inputs,
                                      max_new_tokens=30,
                                      min_new_tokens=10,
                                      do_sample=False,
                                      repetition_penalty=1.01)
output_string = tokenizer.decode(alignment_output_ids[0], skip_special_tokens=True)
print(output_string)

notes += """This looks promising. It isn't always getting it right, but it at least seems to understand the idea and does put newlines in. We can push forward with this then."""
