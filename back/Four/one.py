import numpy as np
from matplotlib import pyplot as plt
from sklearn import linear_model, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error


'''
  生成数据
'''
def createFour(n_samples = 500,n_outliers = 100):
  # 设置噪声和样本数
  n_samples = n_samples  # 样本数
  n_outliers = n_outliers  # 噪声数
  # 生成回归模型数据
  # 构造数据集  sample为样本数 feature为X维度 informative为y维度  noise为数据之间的间隔，高斯噪声
  # coef为系数  random_state是否随机，none的时候随机，参数相当于标记，使得标记相同的时候产生的数据一样
  X, y, coef = datasets.make_regression(n_samples=n_samples, n_features=1, n_informative=1, bias=0, noise=10,
                                        coef=True)
  # x的shape(500,1)  y的shape(500,)
  # 生成噪声点
  #np.random.seed(0)  # 随机数种子，参数表示随机数起始的位置,使得每次生成的噪声点位置一样,使得X，y的生成规律一样
  X[:n_outliers] = 3 + 0.5 * np.random.normal(size=(n_outliers, 1))  # 正态分布，size表示生成(n_outlier, 1)的数组
  y[:n_outliers] = -3 + 10 * np.random.normal(size=n_outliers)  # 截取的是前100个数
  # 3+0.5是让数据点的横坐标以3为中心呈现正态分布，0.5取值是因为横坐标的差值小
  # 对样本进行划分
  # train_test_split函数用于将矩阵随机划分为训练子集和测试子集，并返回划分好的训练集测试集样本和训练集测试集标签。
  global X_train, X_test, y_train, y_test
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
  return X_train,X_test,y_train,y_test


#一元线性回归
def onehg():
  lr = linear_model.LinearRegression()# 创建一个LinearRegression模型
  lr.fit(X_train, y_train) #训练集上训练一个线性回归模型
  global line_X
  line_X = np.arange(X_train.min(), X_train.max())[:, np.newaxis] #增加维度，见下方。作用是平均取点，使得直线更加的直
  #一元线性训练集预测
  line_trainy = lr.predict(line_X) #以LinearRegression的模型预测y
  return line_X,line_trainy

def twohg():
  # 初始化二次多项式生成器
  poly2 = PolynomialFeatures(degree=2)  # 设置多项式阶数为2
  X_train_poly2 = poly2.fit_transform(X_train)  # 用fit_transform将X_train变成2阶
  # 一元二次多项式回归
  lr2 = linear_model.LinearRegression()
  lr2.fit(X_train_poly2, y_train)
  X_train_poly1 = poly2.fit_transform(line_X)
  # 一元二次多项式训练集预测
  line2_trainy = lr2.predict(X_train_poly1)
  return line_X,line2_trainy


def RANSAC(min_samples=10,residual_threshold=25.0,stop_n_inliers=320,max_trials=100):
  ransac = linear_model.RANSACRegressor(base_estimator=linear_model.LinearRegression(),
                                        # base_estimator 仅限于回归估计，默认LinearRegression
                                        min_samples=min_samples, residual_threshold=residual_threshold
                                        , stop_n_inliers=stop_n_inliers,  # 最小样本  残差  内集阈值
                                        max_trials=max_trials, random_state=0)  # 迭代次数
  ransac.fit(X_train, y_train)
  inlier_mask = ransac.inlier_mask_
  outlier_mask = np.logical_not(inlier_mask)  # 自动识别划分内点集和外点集
  line_y_train_ransac = ransac.predict(line_X)

  data1 = []
  data2 = []
  data3 = []
  #plt.scatter(X_train[inlier_mask], y_train[inlier_mask], color='yellowgreen', marker='.')
  for x, y in zip(X_train[inlier_mask], y_train[inlier_mask]):
    data1.append([x[0], y])

  #plt.scatter(X_train[outlier_mask], y_train[outlier_mask], color='gold', marker='.')
  for x, y in zip(X_train[outlier_mask], y_train[outlier_mask]):
    data2.append([x[0], y])

  #plt.plot(line_X, line_y_train_ransac, color='cornflowerblue', label='RANSAC regressor')
  for x, y in zip(line_X,line_y_train_ransac):
    data3.append([x[0], y])

  return data1,data2,data3