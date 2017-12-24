__author__ = 'jurankirihara'
#test for attributetojson class
# from AttributeToJson import JsonSerialize
# from sklearn.linear_model import LogisticRegression,LinearRegression
# from sklearn.datasets import load_iris
# import json
# import os
#
# filename=os.getcwd()
# filename="sampleJsonAttributes"
# path="../JsonModels"
# fullpath = os.path.join(path, filename)
#
# iris = load_iris()
# X, y = iris.data, iris.target
#
# lr = LogisticRegression(multi_class='multinomial', solver='newton-cg')
# lr.fit(X, y)
# ser = JsonSerialize(fullpath,overwrite=False)
# try:
#     ser.data_to_json(lr)
# except Exception as e:
#     raise e
# lr2=ser.json_to_data(LogisticRegression())
# print(lr2.__dict__)
# y_pred=lr2.predict(X)
# print (y_pred)
