import requests
import os
import dotenv
from cachetools import cached, TTLCache

dotenv.load_dotenv()
api = os.environ.get("API")
cache = TTLCache(maxsize=100, ttl=300) 

class GT_API:
    def __init__(self):   
        self.page = 1
        self.plural = f"{api}?populate=normal_attack,chain_skill.Ailment,special_ability,image_urls&pagination[pageSize]=10&sort=name&pagination[page]={self.page}"
        self.singular = f"{api}/"
    
    @cached(cache)
    async def all_heroes(self, page: int) -> list:
        self.page = page
        response = requests.get(self.plural)
        results = response.json()
        return results
    
    @cached(cache)
    async def find_heroes(self, params, page=1):
        self.page = page
        filters = ['name', 'class', 'element', 'party_buff']
        filter_param = ""
        for j, filter in enumerate(filters):
            filter_param += ''+f"&filters[$or][{j}][{filter}][$containsi]={params}"
        response = requests.get(f"{api}?fields[0]=name&pagination[pageSize]=10&sort=name&pagination[page]={self.page}{filter_param}")
        results = response.json()
        return results
    
    @cached(cache)
    async def getHero(self, id):
        response = requests.get(f'{api}/{id}?populate=normal_attack,chain_skill.Ailment,special_ability,image_urls')
        return response.json()

if __name__ == '__main__':
    gt = GT_API()
    print(gt.find_heroes("Melee Atk"))