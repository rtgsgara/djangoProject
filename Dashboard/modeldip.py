import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score,roc_auc_score
from sklearn.utils import resample

def sample(dataframe):
    download=dataframe[dataframe['is_attributed']==1]
    not_download=dataframe[dataframe['is_attributed']==0]
    not_download_downsampled = resample(not_download,replace = False,  n_samples = len(download), random_state = 27)
    df=pd.concat([not_download_downsampled, download])
    return df

def feature_engineering(df):
    df['dow'] = df['click_time'].dt.dayofweek.astype('uint16')
    df['doy'] = df['click_time'].dt.dayofyear.astype('uint16')
    df['hour'] = df['click_time'].dt.hour.astype('uint16')
    features_clicks = ['ip', 'app', 'os', 'device']

    for col in features_clicks:
        col_count_dict = dict(df[[col]].groupby(col).size().sort_index())
        df['{}_clicks'.format(col)] = df[col].map(col_count_dict).astype('uint16')

    features_comb_list = [('app', 'device'), ('ip', 'app'), ('app', 'os')]
    for (col_a, col_b) in features_comb_list:
        df1 = df.groupby([col_a, col_b]).size().astype('uint16')
        df1 = pd.DataFrame(df1, columns=['{}_{}_comb_clicks'.format(col_a, col_b)]).reset_index()
        df = df.merge(df1, how='left', on=[col_a, col_b])
    return df

df=pd.read_csv('train_sample.csv',parse_dates=['click_time'])
df_sampled=sample(df)
df_feature=feature_engineering(df_sampled)

df_feature.drop(['click_time','attributed_time'],axis=1,inplace=True)
X=df_feature.drop(['is_attributed'],axis=1)
y=df_feature['is_attributed']


from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 1337)
classifier=RandomForestClassifier(n_estimators=50,n_jobs=-1)
classifier.fit(X_train, y_train)
predictions = classifier.predict(X_test)
print(confusion_matrix(y_test,predictions))
print('\n')
print(classification_report(y_test,predictions))
print('\n')
print(roc_auc_score(y_test,predictions))
print('\n')
print(accuracy_score(y_test,predictions))


import pickle
file = open('model.pkl', 'wb')
pickle.dump(classifier, file)
