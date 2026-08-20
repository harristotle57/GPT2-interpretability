# AI-DISCLOSURE: ai-autonomous
"""
Stub: does GPT-2 represent emotional valence (happy vs. sad vs. neutral) as
separable structure in the residual stream?

Grounding for why this is worth trying (unlike fine-grained character
counting, this has real precedent on models this size or smaller):
- OpenAI's "sentiment neuron" (Radford et al., 2017) found a single unit
  in a byte-level LSTM -- trained purely as a language model, no sentiment
  labels -- that tracked review sentiment almost perfectly. Valence seems
  to fall out of next-token prediction on its own.
- Turner et al.'s "Activation Addition" (ActAdd) paper builds steering
  vectors on GPT-2 specifically from contrastive word-pair activation
  differences (their example: "Love" vs. "Hate") and shows adding that
  vector to the residual stream reliably shifts generation sentiment.
  This study is close to a direct replication of that setup, aimed at
  characterizing the representation rather than steering with it (yet).

Open design questions to settle before implementing:

1. Bare words vs. words-in-a-carrier-sentence. Feeding "happy" alone is a
   1-token sequence with nothing to condition it -- closer to the word's
   lexical meaning in the abstract than to emotional valence as tracked
   during real generation. Embedding each word in a fixed template (e.g.
   "I feel very {word} today.") and reading the activation at the word's
   position measures emotion-in-context instead, which is more likely to
   be the meaningful quantity. Plan: try bare words first (less code),
   then the templated version if the signal is weak or to confirm it's
   not just a lexical-identity artifact.

2. 3-way (happy/sad/neutral) vs. more emotions. Start with the 3-way
   valence split below. A natural follow-up once that works: add anger
   and/or fear to check whether *discrete* emotions separate even at
   matched valence (is "angry" distinguishable from "sad" -- both
   negative -- or do they collapse onto one good/bad axis?).

3. Word-list confound control. The lists below are kept short, common,
   and matched roughly in register/length across categories, so a probe
   is less likely to be picking up on word frequency or length instead
   of actual valence -- same trap as the Lorem Ipsum memorization issue
   in gpt2_spacing_check.py, different flavor. Some words below (e.g.
   "dispassionate", "unemotional") are long enough to plausibly split
   into multiple GPT-2 BPE tokens -- check with tokenizer.encode(word)
   before assuming one activation vector = one word; mean-pool across
   subword tokens for anything that splits.

Likely method once implemented: reuse the ridge/logistic probe-fitting
machinery already built in initial_linear_probe.py (this is exactly the
kind of code that stays local to the study it was written for until it's
reused a third time) -- extract per-layer activations for each word
(traceformer.loading.load_gpt2()), then check whether a linear probe (or
even just difference-of-means between category centroids) separates the
three categories, and whether NEUTRAL sits between HAPPY and SAD or off
to its own side.
"""

HAPPY = ["happy", "joyful", "cheerful", "delighted", "glad", "pleased",
         "elated", "thrilled", "content", "jolly", "merry", "gleeful",
         "jubilant", "ecstatic", "upbeat"]

SAD = ["sad", "unhappy", "sorrowful", "gloomy", "miserable", "dejected",
       "downcast", "mournful", "melancholy", "despondent", "forlorn",
       "glum", "dismal", "tearful", "somber"]

NEUTRAL = ["calm", "indifferent", "unmoved", "impassive", "detached",
           "composed", "stoic", "apathetic", "dispassionate", "unaffected",
           "unfazed", "blank", "reserved", "unemotional", "placid"]


# TODO: pick up here. Settle the two design questions above, then:
#   - load_gpt2(), extract per-layer hidden states for each word (or
#     each templated sentence) in HAPPY/SAD/NEUTRAL
#   - fit a probe (or start simpler: difference-of-means direction
#     between HAPPY and SAD centroids, check where NEUTRAL projects)
#   - report separability per layer, same shape as initial_linear_probe.py
