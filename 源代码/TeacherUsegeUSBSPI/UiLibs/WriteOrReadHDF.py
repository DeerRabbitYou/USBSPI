#--coding:utf-8--
import h5py
import os

def SaveDatasToHDF(datas,filename,Key):
    if not os.path.exists(filename):
        file = h5py.File(filename, 'w')
    else:
        file = h5py.File(filename, 'a')
    file.create_dataset(Key,data=datas)
    file.close()

def ReadDatasFromHDF(filename,Key):
    file = h5py.File(filename, 'r')
    if Key not in file.keys():
        print("不存在")
        return None,None
    dataset=file[Key]
    return dataset.shape,dataset[:]

# filename='data.h5'
# datas=[i for i in range(20000)]
# import time
# start=time.time()
# SaveDatasToHDF(datas,filename,'1')
# print(str(time.time()-start))
# # # SaveDatasToHDF(datas,filename,'2')
# # # SaveDatasToHDF(datas,filename,'3')
# # shapes,value=ReadDatasFromHDF('RData.h5','test')
# # print(shapes,value[100:])


