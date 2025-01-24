
# BIAS
from flair.models import TARSClassifier
from flair.data import Sentence

def bias_identify(response):
  tar = TARSClassifier.load('tars-base')
  sentence = Sentence(response)
  classes = ["gender stereotype","race stereotype"]
  tar.predict_zero_shot(sentence, classes, multi_label=False)
  score={}
  for i in (list(sentence.get_labels())):
    if i.score>0.5:
      score=i.value
    else:
      score=0

  return  score


