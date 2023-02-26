import requests
import os
import dotenv

dotenv.load_dotenv()
api = os.environ.get("API")

hero_cache = {}
params_cache = {}

class GT_API:
    def __init__(self):   
        self.page = 1
        self.plural = f"{api}?populate=normal_attack,chain_skill.Ailment,special_ability,image_urls&pagination[pageSize]=10&sort=name&pagination[page]={self.page}"
        self.singular = f"{api}/"
        
    
    async def all_heroes(self, page: int) -> list:
        self.page = page
        response = requests.get(self.plural)
        results = response.json()
        return results
    
    async def find_heroes(self, params, page=1):
        if params in params_cache:
            return params_cache[params]
        self.page = page
        filters = ['name', 'class', 'element', 'party_buff']
        filter_param = ""
        for j, filter in enumerate(filters):
            filter_param += ''+f"&filters[$or][{j}][{filter}][$containsi]={params}"
        response = requests.get(f"{api}?fields[0]=name&pagination[pageSize]=10&sort=name&pagination[page]={self.page}{filter_param}")
        results = response.json()
        params_cache[params] = results
        # print(params_cache)
        return results
    
    async def getHero(self, id):
        if id in hero_cache:
            return hero_cache[id]
        response = requests.get(f'{api}/{id}?populate=normal_attack,chain_skill.Ailment,special_ability,image_urls')
        hero_cache[id] = response.json()
        # print(hero_cache)
        return response.json()

if __name__ == '__main__':
    gt = GT_API()
    print(gt.find_heroes("Melee Atk"))