import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_score, recall_score, f1_score
import pymysql

user = "root"
password = "928457"

def function3(max_depth = 8,min_samples_leaf = 18):

    conn = pymysql.connect(host="localhost", user=user, password=password, database="machine")
    iris_data = pd.read_sql("select * from iris", con=conn)

    iris_data = iris_data.dropna()  # 丢弃缺失值

    # --------------用决策树进行划分--------------
    all_inputs = iris_data[['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width']].values
    all_classes = iris_data['Species'].values
    # 划分训练系与测试集
    (training_inputs, testing_inputs, training_classes, testing_classes) = train_test_split(all_inputs, all_classes, test_size=0.2)

    # 使用5折交叉验证方式训练决策树，使用GridSearchCV函数对参数调优，按最优参数调整参数
    parameters = {"max_depth": [*range(1, 5)], 'min_samples_leaf': [*range(1, 6)]}
    clf = DecisionTreeClassifier()
    gs = GridSearchCV(clf, parameters, cv=5)
    gs.fit(training_inputs, training_classes)

    # --------------分别将两棵决策树进行可视化--------------
    plt.figure(figsize=(10, 5))
    plt.gcf().subplots_adjust(left=0.05,top=0.91,bottom=0.09)
    clf = DecisionTreeClassifier(max_depth=max_depth, min_samples_leaf=min_samples_leaf)
    clf.fit(training_inputs, training_classes)
    clf.predict(training_inputs)
    tree.plot_tree(clf, filled=True, feature_names=['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'])
    plt.savefig(r"D:\machine_img\three\1.png")
    plt.show()
    clf2 = gs.best_estimator_
    clf2 = clf2.fit(training_inputs, training_classes)
    clf2.predict(training_inputs)
    tree.plot_tree(clf2, filled=True, feature_names=['Sepal.Length', 'Sepal.Width', 'Petal.Length', 'Petal.Width'])
    plt.savefig(r"D:\machine_img\three\2.png")
    plt.show()
    # -----------------在测试集上计算两棵决策树的precision、recall、F1-measure---------------
    names = ["DecisionTreeClassifier参数调优前", "DecisionTreeClassifier参数调优后"]
    models = [clf, clf2]
    num_list0 = []
    num_list1 = []
    num_list2 = []
    num_list3 = []

    plt.close()

    def compute(name, model):
        y_train_pred = model.predict(training_inputs)
        y_test_pred = model.predict(testing_inputs)
        # precision
        train_precision = precision_score(training_classes, y_train_pred, average='micro')
        test_precision = precision_score(testing_classes, y_test_pred, average='micro')
        # recall
        train_recall = recall_score(training_classes, y_train_pred, average='micro')
        test_recall = recall_score(testing_classes, y_test_pred, average='micro')
        # f1
        train_f1 = f1_score(training_classes, y_train_pred, average='micro')
        test_f1 = f1_score(testing_classes, y_test_pred, average='micro')

        if model == clf:
            num_list0.append([train_precision, train_recall, train_f1])
            num_list1.append([test_precision, test_recall, test_f1])
        else:
            num_list2.append([train_precision, train_recall, train_f1])
            num_list3.append([test_precision, test_recall, test_f1])


    compute(names[0], models[0])
    compute(names[1], models[1])

    data1 = []
    data2 = []
    data1.append(['label','参数调优前','参数调优后'])
    data1.append(['precision',round(num_list0[0][0],2),round(num_list2[0][0],2)])
    data1.append(['recall', round(num_list0[0][1],2), round(num_list2[0][1],2)])
    data1.append(['F1-measure', round(num_list0[0][2],2), round(num_list2[0][2],2)])

    data2.append(['label', '参数调优前', '参数调优后'])
    data2.append(['precision', round(num_list1[0][0],2), round(num_list3[0][0],2)])
    data2.append(['recall', round(num_list1[0][1],2), round(num_list3[0][1],2)])
    data2.append(['F1-measure', round(num_list1[0][2],2), round(num_list3[0][2],2)])

    return data1,data2


if __name__ == '__main__':
    function3()