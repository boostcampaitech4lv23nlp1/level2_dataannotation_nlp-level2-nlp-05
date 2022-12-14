import pickle as pickle
import os
import json
import pandas as pd
import argparse
import numpy as np
import sklearn
from sklearn.metrics import accuracy_score

def klue_re_micro_f1(preds, labels, average):
    """KLUE-RE micro f1 (except no_relation)"""
    label_list = [
    'no_relation',
    'per:propose',
    'clo:revolves',
    'clo:contains',
    'clo:composed_of',
    'clo:turn_into',
    'clo:alias_of',
    'met:feature_of',
    'dat:date_of_discovery',
    'per:origin_of',
    'clo:exists_in']
    no_relation_label_idx = label_list.index("no_relation")
    label_indices = list(range(len(label_list)))
    label_indices.remove(no_relation_label_idx)
    return sklearn.metrics.f1_score(labels, preds, average="micro", labels=label_indices) * 100.0

def klue_re_auprc(probs, labels):
    labels = np.eye(11)[labels]

    score = np.zeros((11,))
    for c in range(11):
        targets_c = labels.take([c], axis=1).ravel()
        preds_c = probs.take([c], axis=1).ravel()
        precision, recall, _ = sklearn.metrics.precision_recall_curve(targets_c, preds_c)
        score[c] = sklearn.metrics.auc(recall, precision)
    return np.average(score) * 100.0

def label_to_num(label):
  num_label = []

  dict_label_to_num = {'no_relation': 0, 'per:propose': 1, 'clo:revolves': 2, 'clo:contains': 3,
                       'clo:composed_of': 4, 'clo:turn_into': 5, 'clo:alias_of': 6, 
                       'met:feature_of': 7, 'dat:date_of_discovery': 8, 'per:origin_of': 9, 
                       'clo:exists_in': 10}
  for v in label:
    num_label.append(dict_label_to_num[v])
  
  return num_label

def make_probs(probs):
  prob_temp = []
  probs = probs.apply(lambda x: x[1:-1].split(','))
  for i in probs:
    prob_temp.append(list(map(float, i)))
  return prob_temp

def evaluation(gt_path, pred_path):

  pred = pd.read_csv(pred_path) # model이 예측한 정답 csv [id,pred_label, probs]
  answer = pd.read_csv(gt_path) # test dataset의 정답 csv [id, label]

  micro_f1 = klue_re_micro_f1(label_to_num(pred["pred_label"]), label_to_num(answer["label"]), average='micro') 
  auprc = klue_re_auprc(np.array(make_probs(pred['probs'])), np.array(label_to_num(answer["label"])))

  results = {}
  results['micro_f1'] = {
        'value': f'{micro_f1:.04f}',
        'rank': True,
        'decs': True,
    }
  results['auprc'] = {
      'value': f'{auprc:.04f}',
      'rank': False,
      'decs': True,
  }

  return json.dumps(results)

def main(args):
  print(evaluation(args.public_dataset_dir, args.pred_answer_dir))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  # data dir
  parser.add_argument('--pred_answer_dir', type=str, default="../data/prediction/submission.csv")
  parser.add_argument('--public_dataset_dir', type=str, default="../data/answer/answer.csv")
  args = parser.parse_args()
  main(args)



