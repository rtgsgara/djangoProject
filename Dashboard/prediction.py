import pickle
import pandas as pd

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


model = pickle.load(open('model.pkl', 'rb'))
df=pd.read_csv('test_new.csv',parse_dates=['click_time'])
test_feature=feature_engineering(df)
time=test_feature[['click_time']]
test_feature.drop(['click_time','click_id'],axis=1,inplace=True)

prediction=model.predict(test_feature)
test_feature['predicted']=prediction
test_feature['click_time']=time
test_predicted=test_feature[['ip','app','device','os','channel','click_time','predicted']]

test_predicted.to_csv('test_final.csv',index=False)
print(test_predicted.head())
