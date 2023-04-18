from flask import Flask,request,jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pymysql
from One import Apriori21
from One import score
from Two.one import create,julei,dbscan
from Three.one import function3
from Four.one import createFour,onehg,twohg,RANSAC

app = Flask(__name__)

user = "root"
password = "928457"

# 启动后端服务
app = Flask(__name__)
# 进行跨域处理
CORS(app,resources=r'/*')


#数据库连接
conn = pymysql.connect(host="localhost",user=user,password=password,database="machine")
cursor = conn.cursor()

#登录接口
@app.route('/login')
def login():
    username =request.args.get("username")
    password = request.args.get("password")
    res = cursor.execute("select * from user where username = %s and password = %s",[username,password])
    # 用户名密码正确返回 1 ， 错误返回 0
    return jsonify({'code':res})

# 关联规则接口
# 接受前端发来三个参数：minSupport，minConfidence，minLift
# 后端根据参数调用关联规则算法，将生成的数据以json格式发给前端
# 前端收到后端发来的数据，进行可视化展示

@app.route('/one')
def one():
    minSupport = float(request.args.get("minSupport"))
    minConf = float(request.args.get("minConf"))
    data,string = Apriori21.load_data(minSupport,minConf)
    result = {'data1': data,'data2':string}
    return jsonify(result)

# 获取购物篮数据接口
# 后端将打分表数据以json格式发给前端
# 前端收到后端发来的数据，进行可视化展示
@app.route('/one/shop')
def loadData_shop():
    dd = pd.read_sql("select * from shop",con=conn)
    data1 = []
    for i, row in dd.iterrows():
        data1.append({'one': str(row[0]), 'two': str(row[1]), 'three': str(row[2]),
                      'four': str(row[3])})
    return jsonify({'data':data1})

# 获取打分表数据接口
# 后端将打分表数据以json格式发给前端
# 前端收到后端发来的数据，进行可视化展示
@app.route('/one/score')
def loadData():
    dd = pd.read_sql("select * from score",con=conn)
    data1 = []
    for i, row in dd.iterrows():
        data1.append({'num': str(row[0]), 'name': str(row[1]), 'ppt': str(row[2]),
                      'jiangjie': str(row[3]), 'answer': str(row[4]), 'class': str(row[5])})
    return jsonify({'data':data1})

# 针对各列评分属性，进行数据统计值分析
# 后端调用打分算法，将生成的数据以json格式发给前端
# 前端收到后端发来的数据，进行可视化展示

@app.route('/two')
def two():
    quality, lecture, answer,dd1,dd2 = score.func()
    data1 = []
    data1.append({'value':quality[0],'name':'A'})
    data1.append({'value': quality[1], 'name': 'B'})
    data1.append({'value': quality[2], 'name': 'C'})
    data1.append({'value': quality[3], 'name': 'D'})
    data2 = []
    data2.append({'value': lecture[0], 'name': 'A'})
    data2.append({'value': lecture[1], 'name': 'B'})
    data2.append({'value': lecture[2], 'name': 'C'})
    data2.append({'value': lecture[3], 'name': 'D'})
    data3 = []
    data3.append({'value': answer[0], 'name': 'A'})
    data3.append({'value': answer[1], 'name': 'B'})
    data3.append({'value': answer[2], 'name': 'C'})
    data3.append({'value': answer[3], 'name': 'D'})
    return jsonify({'data1':data1,'data2':data2,'data3':data3,'data4':dd1,'data5':dd2})


# 聚类数据生成接口
# 接受前端发来四个个参数：num，noise，centers，cluster_std
# 后端根据参数调用聚类数据生成算法，生成相应的图片保存到本地
# 前端显示保存到本地的图片
@app.route('/two/one/create')
def autocreate():
    num = int(request.args.get("num"))
    noise = float(request.args.get("noise"))
    centers = int(request.args.get("centers"))
    cluster_std = float(request.args.get("cluster_std"))
    create(num,noise,centers,cluster_std)
    return jsonify({'code':200})


# 聚类接口
# 接受前端发来的一个参数：k : 聚类个数
# 后端根据参数调用聚类算法，生成相应的图片保存到本地
# 前端显示保存到本地的图片
@app.route('/two/one/julei')
def jul():
    k = int(request.args.get("k"))
    julei(k)
    return jsonify({'code':200})


# dbscan聚类接口
# 接受前端发来的两个参数：eps ,min_samples
# 后端根据参数调用dbscan聚类算法，生成相应的图片保存到本地
# 前端显示保存到本地的图片
@app.route('/two/one/dbscan')
def dbsc():
    eps = float(request.args.get("eps"))
    min_samples = int(request.args.get("min_samples"))
    dbscan(eps,min_samples)
    return jsonify({'code':200})

# 获取iris2.csv数据接口
# 后端读取iris2.csv数据，以json格式发送给前端
# 前端接收数据并进行显示
@app.route('/three/iris')
def loadData4():

    dd = pd.read_sql("select * from iris", con=conn)
    data1 = []
    for i, row in dd.iterrows():
        data1.append({'num': str(row[0]), 'name': str(row[1]), 'ppt': str(row[2]),
                      'jiangjie': str(row[3]), 'answer': str(row[4]), 'class': str(row[5])})
    return jsonify({'data':data1})

# 决策树生成接口
# 接受前端发来的两个参数：max_depth ,min_samples_leaf
# 后端调用决策树生成算法，将算法生成的数据以json格式发给前端
# 前端收到后端发来的数据，进行可视化展示
@app.route('/three/create')
def func3():
    max_depth = int(request.args.get("max_depth"))
    min_samples_leaf = int(request.args.get("min_samples_leaf"))
    data1,data2 = function3(max_depth,min_samples_leaf)
    return jsonify({'data1':data1,'data2':data2})

# 回归数据生成接口
# 接受前端发来的两个参数：n_samples ,n_outliers
# 后端根据参数调用回归数据生成算法，以json格式发送给前端，数据包括训练集数据和测试集数据
# 前端接收数据并进行显示
@app.route('/four/create')
def func4():
    n_samples = int(request.args.get("n_samples"))
    n_outliers = int(request.args.get("n_outliers"))
    X_train, X_test, y_train, y_test = createFour(n_samples,n_outliers)
    train = []
    test = []
    for x,y in zip(X_train,y_train):
        train.append([x[0],y])
    for x,y in zip(X_test,y_test):
        test.append([x[0],y])
    return jsonify({'train':train,'test':test})

# 回归接口
# 后端调用一元、二元回归算法，算法生成的数据以json格式发送给前端
# 前端接收数据并进行显示
@app.route('/four/huihui')
def func5():
    line_X,line_trainy = onehg()
    line_X2, line2_trainy = twohg()
    data1 = []
    data2 = []
    for x,y in zip(line_X,line_trainy):
        data1.append([x[0],y])
    for x,y in zip(line_X2,line2_trainy):
        data2.append([x[0],y])
    return jsonify({'data1':data1,'data2':data2})

# ransac回归接口
# 接受前端发来的四个参数：min_samples ,residual_threshold，stop_n_inliers，max_trials
# 后端根据参数调用ransac回归算法，将生成的数据以json格式发送给前端
# 前端接收数据并进行显示
@app.route('/four/ransac')
def func6():
    min_samples = int(request.args.get("min_samples"))
    residual_threshold = float(request.args.get("residual_threshold"))
    stop_n_inliers = int(request.args.get("stop_n_inliers"))
    max_trials = int(request.args.get("max_trials"))
    data1, data2, data3 = RANSAC(min_samples,residual_threshold,stop_n_inliers,max_trials)
    return jsonify({'data1':data1,'data2':data2,'data3':data3})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
    print("Good Bye")


