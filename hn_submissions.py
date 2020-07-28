import requests
import pygal
from operator import itemgetter

url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print('Status code:', r.status_code)

submission_ids = r.json()
submission_dicts = []
names = []
for submission_id in submission_ids[:30]:
    # Make a separate API call for each submission.
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
            str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()
    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)
        }
    submission_dicts.append(submission_dict)
    names.append(response_dict['title'])

submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                                    reverse=True)
for submission_dict in submission_dicts:
    print("\nTitle:", submission_dict['title'])
    print("Discussion link:", submission_dict['link'])
    print("Comments:", submission_dict['comments'])

#Graphing stuff----------------------------------------------------------------
names = []
graph_list = []
for submission_id in submission_ids[:30]:
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
            str(submission_id) + '.json')
    submission_r = requests.get(url)
    response_dict = submission_r.json()
    submission_dict = {
        'value': response_dict.get('descendants', 0),
        'label': response_dict['title'],
        'xlink': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        }
    graph_list.append(submission_dict)
    names.append(response_dict['title'])

graph_list = sorted(graph_list, key=itemgetter('value'),
                                  reverse=True)

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(my_config, x_label_rotation=45, show_legend=False)
chart.title = 'Most active disscusions on Hacker News'
chart.x_labels = names
chart.add('', graph_list)
chart.render_to_file('Desktop/Coding_Projects/Working_With_APIs/hn_visual.svg')
print('A popularity graph for the language has been made')

#Here we use requests again, this time calling Hacker News
#The first call returns the 500 most popular articles on the website
#we then loop through 30 of the most popular of those, creating a nice index of-
#- popular articles
