import pandas as pd
import numpy as np
import csv

from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.metrics import precision_recall_fscore_support

def train_and_report():
    df = pd.read_csv("sequence_data.csv")
    X = df.drop('CLASS', axis=1)
    y = df['CLASS']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
    svclassifier = SVC(kernel='rbf', gamma=10)
    svclassifier.fit(X_train, y_train)

    y_pred = svclassifier.predict(X_test)
    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test, y_pred))

    metrics = precision_recall_fscore_support(y_test, y_pred, average='weighted')

    return metrics[0], metrics[1], metrics[2]

def run_n_report(num_of_trials):
    with open('results_45_min.csv', mode='w') as results:
        seq_writer = csv.writer(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)

        header = ["Precision", "Recall", "F1-score"]
        seq_writer.writerow(header)

        prec_sum, recall_sum, fscore_sum = 0, 0, 0
        for i in range(num_of_trials):
            prec, recall, fscore = train_and_report()
            prec_sum += prec
            recall_sum += recall
            fscore_sum += fscore

            new_line = [prec, recall, fscore]
            seq_writer.writerow(new_line)

        average_header = ["Avg Precision", "Avg Recall", "Avg Fscore"]
        seq_writer.writerow(average_header)

        averages = [prec_sum/num_of_trials,
                    recall_sum/num_of_trials,
                    fscore_sum/num_of_trials]
        seq_writer.writerow(averages)

if __name__ == "__main__":
    run_n_report(30)
