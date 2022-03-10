import pandas as pd

column_names = ['movie_name', 'rating', 'director_1',
                'director_2', 'actor_1', 'actor_2', 'actor_3', 'actor_4']

def make_node_list():
    df = pd.read_csv('movies_network.csv')
    actor_names = df[['Actor 1', 'Actor 2', 'Actor 3', 'Actor 4']]
    actor_numbers = actor_names.stack().rank(method='dense').unstack().dropna().astype(int)
    temp = actor_numbers[(actor_numbers == 156).any(axis=1)]
    column_names = ['actor_id', 'actor_name']
    df = pd.DataFrame(columns=column_names)

    for i in range(1, 5539):
        print(i)
        temp = actor_numbers[(actor_numbers == i).any(axis=1)]
        if len(temp) == 0:
            continue
        row = temp.index[0] 

        for j in range(4):
            if actor_numbers.loc[row][j] == i:
                column = j
        name = actor_names.iloc[row][column]
        df = df.append({'actor_id': actor_numbers.loc[row][column], 'actor_name': name}, ignore_index=True)
    df.to_csv('actor_labels.csv', index=False)

    
def make_edge_list():
    df = pd.read_csv('movies_network.csv')
    actor_values = df[['Actor 1', 'Actor 2', 'Actor 3', 'Actor 4']]
    actor_indi = actor_values.stack().rank(method='dense').unstack().dropna().astype(int)
    col_names = ['source', 'target']
    network_dataframe = pd.DataFrame(columns=col_names)
    for  i in range(1, actor_indi.max().max()):
        search_actor = actor_indi[(actor_indi == i).any(axis=1)].values
        for row in range(len(search_actor)):
            for col in range(4):
                if search_actor[row][col] != i:
                       network_dataframe = network_dataframe.append({'source': i, 'target': search_actor[row][col]}, ignore_index=True)
            
    network_dataframe.to_csv('network_dataframe.csv', index=False)
    
if __name__ == '__main__':
    make_node_list()
    make_edge_list()
