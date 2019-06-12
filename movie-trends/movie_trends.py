from apikeys import TMDB_KEY
from datetime import datetime
from bokeh.plotting import figure, output_file, show
import calendar
import requests
import json
from bokeh.palettes import all_palettes
import itertools

#fetch the list of genre from API
def get_list_genre(api_key):
    res = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key="+TMDB_KEY)
    data = res.text
    parsed = json.loads(data)
    return parsed['genres']

#return the releases of every month for every genre by calling API
def releases_genre_month(genre): 
    genre1 = genre
    year = 2018
    result = {} 
    print("\nFetching the data")
    for i in range(1,13):
        s,e = calendar.monthrange(year,i)
        start_date = str(year)+"-"+str(i)+"-1"
        end_date = str(year)+"-"+str(i)+"-"+str(e)
        format_str = "%Y-%m-%d"
        mydate = datetime.strptime(start_date,format_str)
        month_name = mydate.strftime("%b")
        count = 0
        response= requests.get("https://api.themoviedb.org/3/discover/movie?api_key="+TMDB_KEY+"&with_genres="+str(genre1)+"&primary_release_year="+str(year)+"&primary_release_date.gte="+start_date+"&primary_release_date.lte="+end_date)
        data1 = response.text
        parsed1 = json.loads(data1)
        count = parsed1['total_results']    
        result[month_name] = count
    print("------- \n", end ="", flush = True)
    return result

#calculate the total releases for every genre every month
def calculate_total_releases(ans):
    response=requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key="+TMDB_KEY)
    data = response.text
    parsed = json.loads(data)
    output = {}
    anss = ans
    #for every genre entered by the user finding the releases
    for x in anss:
        for val in parsed.values():
            for elem in val:
                name = elem['name']
                name = name.lower()
                if x == name:
                    genre_id=elem['id']
                    genre_name = elem['name']
                    res = releases_genre_month(genre_id)
                    output[genre_name] = res                        
    return output
       
#Function to plot the graph
def visualization(get_master):
    year = 2018
    palette=['mediumvioletred','green','yellow','crimson','slateblue','midnightblue','slategray','mediumblue','chocolate','darkcyan','tomato','lightseagreen','deeppink','cornflowerblue','olive']
    output_file("genre_by_season.html")
    x_val = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]
    p = figure(x_range = x_val, title = "Releases by genre: "+str(2018))
    p.yaxis.axis_label = "Releases"
    p.xaxis.axis_label = "Month"
    j=0
    for key,elem in get_master.items():
        list_count = []
        key_l = key
        for val in elem.values():
            list_count.append(val)
        p.line(x_val,list_count,line_color=palette[j], legend= key_l, line_width=2)
        j=j+1
    show(p)

#main function 
def main():

    print("The following Genres are available to find out the movie releases by genre!\n")
    list_genre = get_list_genre(TMDB_KEY)
    genre_names = []
    for elem in list_genre:
        name = elem['name']
        genre_names.append(name.lower())
        print(elem['name'])
    print("Please enter the genres for which you would like to see the plot or end to stop entering values")
    list_user_input = []
    user_input = ''
    while(user_input!='end'):
        user_input = input('-->')
        user_input =user_input.lower()
        if user_input in genre_names:
            list_user_input.append(user_input)
        elif user_input=='end':
            print("Thank you for entering the values")
        else:
            print('Please enter correct input which matches the names displayed in the genre list or enter end to stop')
    print(list_user_input)
    get_master = calculate_total_releases(list_user_input)   
    print("Data has been fetched")
    visualization(get_master)   

if __name__ == '__main__':
     main() 