from __future__ import print_function, division

__author__ = 'amrit'

from transformation import *
from random import seed
from utilities import _randchoice, unpack
from ML import *
from itertools import product
#from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from demos import *
import pickle

preprocess=[standard_scaler,minmax_scaler, maxabs_scaler,[robust_scaler]*20,kernel_centerer,[quantile_transform]*200
            ,normalizer,[binarize]*100] #,[polynomial]*5
MLs=[NB,[KNN]*20,[RF]*50,[DT]*30,[LR]*50] #[SVM]*100,
preprocess_list=unpack(preprocess)
MLs_list=unpack(MLs)
combine=[[r[0],r[1]] for r in product(preprocess_list,MLs_list)]
metrics=["Dist2Heaven","popt20"]

def readfile(path=""):
    df=pd.read_csv(path)
    return df

def _test(res=''):
    np.random.seed(500)
    seed(500)
    df=readfile("../data/defect/"+res+".csv")
    metric="popt20"

    final = {}
    e_value = [0.025, 0.05, 0.1, 0.2]

    for e in e_value:
        func_str_dic = {}
        func_str_counter_dic = {}
        lis_value = []
        dic_median = {}
        for i in combine:
            scaler, tmp1 = i[0]()
            model, tmp2 = i[1]()
            string1 = tmp1 + "|" + tmp2
            func_str_dic[string1] = [scaler, model]
            func_str_counter_dic[string1] = 0

        counter=0
        while counter!=1000:
            # func_str_counter_dic=OrderedDict(sorted(func_str_counter_dic.items(), key=itemgetter(1)))
            keys=[k for k, v in func_str_counter_dic.items() if v == 0]
            key=_randchoice(keys)
            try:
                scaler,model=func_str_dic[key]
                df1=transform(df,scaler)

                sss = StratifiedShuffleSplit(n_splits=1, test_size=0.2)
                data,labels=df1[df1.columns[:-2]], df1[df1.columns[-2]]
                for train_index, test_index in sss.split(data,labels):
                    train_data, test_data=df1.iloc[train_index], df1.iloc[test_index]
                    measurement=run_model(train_data,test_data,model,metric)

                    if all(abs(t-measurement)>e for t in lis_value):
                        lis_value.append(measurement)
                        func_str_counter_dic[key] += 1
                    else:
                        func_str_counter_dic[key] += -1

                    dic_median[counter]=max(lis_value)
                counter+=1
            except:
                pass

        final[e]=dic_median
    print(final)
    with open('../dump/popt20_' + res + '.pickle', 'wb') as handle:
        pickle.dump(final, handle)

if __name__ == '__main__':
    eval(cmd())