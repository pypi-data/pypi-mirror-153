#preprocessing

def backtesting_pp2(data, path):

    #data.drop(['Unnamed: 0', 'BTC_close', 'DXY', 'BTCD', 'Kimchi_premium','S&P500','Ethereum DeFi','News_freq', 'signal'], axis=1, inplace=True)
    #data['Date'] = pd.to_datetime(data['Date'])
    
    data.set_index('Date',inplace=True)
    
    
    data['u'] = (data['pred_labels'] ==0)
    data['d'] = (data['pred_labels'] ==1)
    data['h'] = (data['pred_labels']==2)
    
    up_list = []
    prev_val = False

    for inx, val in data['u'].iteritems():
        if prev_val != val:
            if val:
                start = inx
            else:
                up_list.append((start, inx))

        prev_inx = inx
        prev_val = val

    data.reset_index(drop=False, inplace=True)  
    data.insert(5, 'up', -1)


    for i,j in up_list:
        data.loc[data['Date']== i, ['up']] = -2
        data.loc[data['Date']== j, ['up']] = -3
        
    data.set_index('Date',inplace=True)
    data.drop(['pred_labels','u','d', 'h'], axis=1, inplace=True)
    
    #data.drop(['se'], axis=1, inplace=True)
    #data.insert(7, 'se', 0)
    #data.se.iloc[0] = 1
    #data.se.iloc[-1] = 2
    
    data= data.astype({'Open':float, 'High':float, 'Low':float, 'Close':float})
    #data= data.astype({'se':float})
    
    data.to_csv(path)

    return data