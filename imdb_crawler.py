from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_movies_names(soup):
    movies_list = soup.select('h3.lister-item-header a')
    return [movies_list[i].text for i in range(len(movies_list))]

def get_ratings(soup):
    li = soup.select('div.lister-item-content')
    ratings = []
    for i in range(len(li)):
        string = li[i].select('div.ipl-rating-star.small span.ipl-rating-star__rating')   
        if len(string) == 0:
            ratings.append('') 
        else:
            ratings.append(str(string).split('<')[-2].split('>')[1])
    return ratings

def get_celeb_names(soup):
    name_list = soup.select('div.lister-item-content p.text-muted.text-small')
    director_1 = []
    director_2 = []
    actor_1 = []
    actor_2 = []
    actor_3 = []
    actor_4 = []

    for i in range( len(name_list)):
        if 'Stars' in name_list[i].text or 'Director' in name_list[i].text:
            if 'Director' in name_list[i].text:
                text = name_list[i].text
                director_1.append(text.split('Stars:')[0].split('\n')[2])
                
                if len(text.split('Stars:')[0].split('\n')) >= 5:
                    if text.split('Stars:')[0].split('\n')[4].split(',')[0] == '    ':
                        director_2.append('')
                    else:
                        director_2.append(text.split('Stars:')[0].split('\n')[4].split(',')[0])
                else:
                    director_2.append('')
            else:
                director_1.append('')
                director_2.append('')
            
            if 'Stars' in name_list[i].text:         
                text = name_list[i].text.split('Stars:')[1].split('\n')
                actor_1.append(text[1].split(',')[0])
                actor_2.append(text[2].split(',')[0])
                actor_3.append(text[3].split(',')[0])
                if len(text) >= 5:
                    actor_4.append(text[4].split(',')[0])
                else:
                    actor_4.append('')
            else:
                actor_1.append('')
                actor_2.append('')
                actor_3.append('')
                actor_4.append('')  
                
    return director_1, director_2, actor_1, actor_2, actor_3, actor_4       

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    
    movies_names = get_movies_names(soup)
    ratings = get_ratings(soup)
    director_1, director_2, actor_1, actor_2, actor_3, actor_4 = get_celeb_names(soup)

    column_names = ['Movie', 'Rating','Director 1','Director 1', 'Actor 1', 'Actor 2', 'Actor 3', 'Actor 4']
    df = pd.DataFrame(list(zip(movies_names, ratings,director_1, director_2, actor_1, actor_2, actor_3, actor_4)), columns=column_names)
    return df

def main():
    df = pd.DataFrame()
    URLS = ['https://www.imdb.com/list/ls048276758/?ref_=otl_2&sort=list_order,asc&st_dt=&mode=detail&page=',
            'https://www.imdb.com/list/ls090245754/?sort=list_order,asc&st_dt=&mode=detail&page=']
    
    number_of_pages = 10
    for url in URLS:
        for i in range(1,number_of_pages + 1):
            df = df.append(get_data(url + str(i)))
            
    df.to_csv('movies_network.csv', index=False)
    
if __name__ == "__main__":
    main()