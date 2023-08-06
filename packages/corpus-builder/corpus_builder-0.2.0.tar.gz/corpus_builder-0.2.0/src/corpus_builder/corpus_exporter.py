import csv
import json
import pickle

def export_to_json(corpus, json_file):
    with open(json_file, 'w') as f:
        f.write(json.dumps(corpus, indent=4))

def export_to_pickle(corpus, pickle_file):
    with open(pickle_file, 'wb') as f:
        pickle.dump(corpus, f)

def export_to_csv(corpus, csv_file):
    classes_names = _get_classes_names(corpus)
    columns = ['sentence'] + classes_names + ['entities']
    with open(csv_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        for sentence, annotations in corpus:
            labels = [annotations[cl] if cl in annotations else '' for cl in classes_names]
            row = [sentence] + labels + [str(annotations['entities'])]
            writer.writerow(row)

def _get_classes_names(corpus):
    names = set()
    for sent, annot in corpus:
        classes = annot.copy()
        classes.pop('entities')
        names.update(classes.keys())
    return list(names)