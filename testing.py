from dotenv import dotenv_values
from sentence_transformers import SentenceTransformer, util

from wiki import Wikipedia

secrets = dotenv_values('.env')
api = Wikipedia(
    secrets['AccessToken'],
    'Testing',
    'en'
)
model = SentenceTransformer('all-MiniLM-L6-v2')

start = 'https://en.wikipedia.org/wiki/Main_battery'
goal = 'https://en.wikipedia.org/wiki/Lego'


goal_title = goal.split('/')[-1]
goal_embed = model.encode(goal_title)

cur = start.split('/')[-1]
visited = set([])

for i in range(100):
    visited.add(cur)
    print(i, cur)
    links = api.page_links(cur)
    link_embed = model.encode(links)

    best_score = float('-inf')
    best_pick = None
    for i in range(link_embed.shape[0]):
        sim = util.cos_sim(goal_embed, link_embed[i])
        if links[i] not in visited and sim >= best_score:
            best_score = sim
            best_pick = links[i]
    
    cur = best_pick
    if cur == goal_title:
        print(f'Found {cur}')
        break
