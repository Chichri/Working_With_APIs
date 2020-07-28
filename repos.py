import requests
import pygal
lang = input('Which language would you like information on?\n')
url = 'https://api.github.com/search/repositories?q=language:' + str(lang) + '&sort=stars'
r = requests.get(url)
print('Status code:', r.status_code)
response_dict = r.json()
print(response_dict.keys())
#The requests package allows python to easily make api calls
#Here, we store the url of an API call in variable url
#Then, r is assigned to the response object of that url call
#With this, we can work with the response objects attributes and methods
#r.status_code here return 200, which is the code for a successful response
#json() converts the JSON formatted response into a python dictionary

print('\n')

print('Total repositories:', response_dict['total_count'])

repo_dicts = response_dict['items']
print('Repositories returned:', len(repo_dicts))

repo_dict = repo_dicts[0]
print('\nKeys:', len(repo_dict))
for key in sorted(repo_dict.keys()):
    print(key)
#Here we start to work a little harder with the response_dict
#The first print() prints the total of every single asked for repository
#Then we single out the first dictionary in repo_dicts
#The second print() checks how many keys are in this first dict
#The following for loops through the list of keys and prints each individual key

print('\n')

def info_spill(repo_dict):
    print('Name:', repo_dict['name'])
    print('Owner:', repo_dict['owner']['login'])
    print('Stars:', repo_dict['stargazers_count'])
    print('Repository:', repo_dict['html_url'])
    print('Created:', repo_dict['created_at'])
    print('Updated:', repo_dict['updated_at'])
    print('Description:', repo_dict['description'])
#All of this is just picking information from the selected repo
print("Selected information about the first repository: \n")
info_spill(repo_dict)
#This call uses the first, and currently most starred, python repo
#It returns the value of every key specified in info_spill()

for repo_dict in repo_dicts:
    info_spill(repo_dict)
#Now we're just looping through the few repositories we have access to

names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])
    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': repo_dict['description'],
        'xlink': repo_dict['html_url'],
        }
    plot_dicts.append(plot_dict)

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
chart.title = 'Most-Starred '+ str(lang) +' Projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file('Desktop/Coding_Projects/Working_With_APIs/repos.svg')
print('A popularity graph for the language has been made')
