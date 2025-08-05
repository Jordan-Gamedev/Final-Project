from subprocess import Popen

class Biome:

    def __init__(self, name:str, initial_price:int, starting_expand_price:int, expand_price_hike_mult:int, starting_size:int, size_increment:int, max_size:int):
        
        # biome pricing
        self.initial_price = initial_price
        self.starting_expand_price = starting_expand_price
        self.expand_price_hike_mult = expand_price_hike_mult
        self.times_purchased = 0
        
        # biome stats
        self.name = name
        self.starting_size = starting_size,
        self.size_increment = size_increment
        self.max_size = max_size
        self.subprocess:Popen = None

    def __del__(self):
        self.close_biome()

    def get_price(self) -> int:
        if self.times_purchased == 0:
            return self.biome_price
        else:
            return int(self.starting_biome_expand_price * (self.biome_expand_price_hike_mult ** (self.times_purchased - 1)))
        
    def obtain(self) -> bool:

        # only obtain if it still has room to expand
        if self.get_size() < self.max_size:
            
            # biome just purchased
            self.times_purchased += 1

            # open the biome on first purchase
            if self.times_purchased == 1:
                self.open_biome()
            
            # successfully obtained
            return True
        # already obtained at max size
        else:
            return False
    
    def get_size(self):
        return min(self.starting_size + (self.size_increment * (self.times_purchased - 1)), self.max_size)
    
    def open_biome(self):
        if self.subprocess == None and self.times_purchased > 0:
            self.subprocess = Popen(["python", "Scripts\\biome_process.py", self.name])

    def close_biome(self):
        if self.subprocess != None:
            self.subprocess = self.subprocess.kill()