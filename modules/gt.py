import requests
import os
import dotenv

dotenv.load_dotenv()
api = os.environ.get("API")

hero_cache = {}
params_cache = {}

class GT_API:
    def __init__(self):   
        self.plural = f"{api}/heroes"
        self.singular = f"{api}/hero"
        
    async def all_heroes(self) -> list:
        response = requests.get(self.plural)
        results = response.json()
        return results
    
    async def find_heroes(self, params):
        if params in params_cache:
            return params_cache[params]
        response = requests.get(f"{self.plural}/{params}")
        results = response.json()
        params_cache[params] = results
        # print(params_cache)
        return results
    
    async def getHero(self, id):
        if id in hero_cache:
            return hero_cache[id]
        response = requests.get(f'{self.singular}/{id}')
        hero_cache[id] = response.json()
        # print(hero_cache)
        return response.json()

if __name__ == '__main__':
    gt = GT_API()
    print(gt.find_heroes("Melee Atk"))