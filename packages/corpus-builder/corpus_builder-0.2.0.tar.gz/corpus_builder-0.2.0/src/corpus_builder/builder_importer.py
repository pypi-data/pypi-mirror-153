import ast

from corpus_builder.builder import CorpusBuilder
from corpus_builder.exceptions import InvalidRuleException
from corpus_builder.grammar import Grammar
from corpus_builder.rule import Rule

DELIMITER = '='
ANNOTATION_DELIMITER = ':'
CLASS_MARK = '[class]\n'
ENTITY_MARK = '[entity]\n'

def from_text_file(filename):
    with open(filename, 'r') as f:
        rules = read_rules(f)
        classes_labels = read_classes_labels(f)
        entities_labels = read_entities_labels(f)

    root = rules[0].key
    grammar = Grammar(rules, root)
    builder = CorpusBuilder(grammar, classes_labels, entities_labels)
    return builder

def read_rules(f):
    rules = []
    for line in f:
        # skip comment line
        if line == '\n' or line.startswith('#'):
            continue
        if line == CLASS_MARK:
            return rules
        rules.append(create_rule(line))
    return rules

def create_rule(line):
    try:
        idx = line.index(DELIMITER)
        key = ast.literal_eval(line[:idx].strip())
        derivation = ast.literal_eval(line[idx+1:].strip())
        return Rule(key, derivation)
    except:
        raise InvalidRuleException('Could not create derivation rule from line: ' + line)

def read_classes_labels(f):
    classes_labels = {}
    for line in f:
        if line == '\n' or line.startswith('#'):
            continue
        if line == ENTITY_MARK:
            return classes_labels
        classes_labels.update(create_class_annotation(line))
    return classes_labels

def create_class_annotation(line):
    if ANNOTATION_DELIMITER not in line:
        raise InvalidRuleException('Could not create class annotation from line: ' + line)
    idx = line.index(ANNOTATION_DELIMITER)
    key = ast.literal_eval(line[:idx].strip())
    classes = ast.literal_eval(line[idx+1:].strip())
    return {key: classes}

def read_entities_labels(f):
    entities_labels = {}
    for line in f:
        if line == '\n' or line.startswith('#'):
            continue
        entities_labels.update(create_entity_annotation(line))
    return entities_labels

def create_entity_annotation(line):
    if ANNOTATION_DELIMITER not in line:
        raise InvalidRuleException('Could not create entity annotation from line: ' + line)
    idx = line.index(ANNOTATION_DELIMITER)
    key = ast.literal_eval(line[:idx].strip())
    label = ast.literal_eval(line[idx+1:].strip())
    return {key: label}