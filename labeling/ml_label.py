import pickle
import pandas as pd

def ml_label(date):
    pickle_file = '/home/ec2-user/newsfeeds/main/pickle_file.pkl'
    model_ = pickle.load(open(pickle_file, 'rb'))
    model=model_[0]
    fitted_vectorizer = model_[1]

    data = {'Label':['Funding', "M&A", 'Growth Equity','IPO','Noise'],
            'Label_id':[0,1,2,3,4]}
    category_id_df = pd.DataFrame(data)
    
    file = "database_{}".format(date)
    df = pd.read_csv("/home/ec2-user/newsfeeds/tmp/{}.csv".format(file), error_bad_lines=False)
    articles = df['Article_Name'].values.tolist()
    pred_Y = []
    for article in articles:
        pred=model.predict(fitted_vectorizer.transform([article]))
        pred_Y.append(category_id_df.query('Label_id=={}'.format(pred))['Label'].iloc[0])

    se = pd.Series(pred_Y)
    df['ML_label_Article_Name'] = se.values
    df = df.sort_values(['ML_label_Article_Name', 'Date_Collected'])
    header = ['ML_label_Article_Name','Article_Name','Source','Article_Link','Description','Batch','Date_Collected','Date_Published','Keyword_label_article_name','Keyword_label_description','ER_Spacy']
    df.to_csv("/home/ec2-user/newsfeeds/tmp/{}_.csv".format(file), columns = header, index=False)
