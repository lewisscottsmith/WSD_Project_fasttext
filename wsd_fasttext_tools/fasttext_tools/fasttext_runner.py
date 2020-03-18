import json
import fasttext as ft
from sklearn import metrics

from time import sleep

def get_model(training_data):
    m = ft.train_supervised(training_data, pretrainedVectors='wiki-news-300d-1M.vec', dim=300, epoch=25, lr=1.0,) ######
    sleep(1)
    return m


def predict(model, sentence, k=1):
    out = model.predict(sentence, k=k)
    if k == 1:
        out = out[0]
    return out[0]


def test_model(model, test_data_path, output_path=None, training_data_path=None):
    num_correct = 0
    num_incorrect = 0
    count = 0
    correct = []
    incorrect = []
    # initialise label data
    label_data = {}
    for l in model.labels:
        label_data[l] = {
            "num_correct": 0,
            "num_incorrect": 0,
            "total": 0
        }


    # Getting stats from the training data that was used (Not needed to run the actual tests)
    avg_training_data_num_words = 'n/a'
    if training_data_path is not None:
        with open(training_data_path) as f:
            f_data = f.read()
            training_data_from_file = f_data.split("\n")

        train_data_num_words_count = 0
        train_data_num_words_sum = 0

        for data in training_data_from_file:
            if data == '': break
            label = data.split(" ")[0]
            sentence = data.replace(label, '')
            num_words = len(sentence.split())
            train_data_num_words_count += 1
            train_data_num_words_sum += num_words

        avg_training_data_num_words = train_data_num_words_sum / train_data_num_words_count



    with open(test_data_path) as f:
        f_data = f.read()
        test_data_from_file = f_data.split("\n")

    test_data_num_words_count = 0
    test_data_num_words_sum = 0


    f1score_correct_labels = []#################
    f1score_predicted_labels = []#########

    for data in test_data_from_file:
        #         For each line in the test data
        #       format of data is __label__label__ sentence...
        if data == '': break
        label = data.split(" ")[0]
        sentence = data.replace(label, '')
        prediction = predict(model, sentence)
        num_words = len(sentence.split())
        test_data_num_words_count += 1
        test_data_num_words_sum += num_words
        labels = model.labels
        f1score_correct_labels.append(labels.index(label)) ########
        f1score_predicted_labels.append(labels.index(prediction))#########
        if prediction == label:
            #             Correct label found
            count += 1
            num_correct += 1
            correct.append({
                "data": sentence,
                "label": label,
                "predicted label": prediction,
                "num words": num_words
            })
            label_data[label]['num_correct'] += 1
            label_data[label]['total'] += 1

        else:
            #         prediction is wrong
            count += 1
            num_incorrect += 1
            incorrect.append({
                "data": sentence,
                "label": label,
                "predicted label": prediction,
                "num words": num_words
            })
            label_data[label]['num_incorrect'] += 1
            label_data[label]['total'] += 1

    results = {
        "num_correct": num_correct,
        "num_incorrect": num_incorrect,
        "percentage_correct": "{}%".format((num_correct / count) * 100),
        "f1score (macro)": str(metrics.f1_score(y_true=f1score_correct_labels, y_pred=f1score_predicted_labels, average='macro')),################
        "f1score (weighted)": str(
            metrics.f1_score(y_true=f1score_correct_labels, y_pred=f1score_predicted_labels, average='weighted')),
    ################
        "total": count,
        "result_data": {
            "correct": correct,
            "incorrect": incorrect
        },
        "label_data": label_data,
        "avg num words (test data)": test_data_num_words_sum / test_data_num_words_count,
        "avg num words (training data)": avg_training_data_num_words
    }

    if output_path is not None:
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=4)

    return results


def interactive(model):
    while True:
        x = input(">")
        if x == "stop" or x == "exit":
            break
        print(predict(model, x))


#######################################################################################################################

# m = get_model(club)
# r = test_model(m, "club-test/club-data/club-testing-data.txt", output_path='TMP-OUPUT.json')

# predict(m,"welcome to the club", k=2)
