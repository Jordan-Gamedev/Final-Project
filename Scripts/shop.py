from biome import Biome
from io import TextIOWrapper
import os
from pyray import file_exists

def open_save_file() -> TextIOWrapper:
        
        # make this process wait for the saving process to finish
        while not file_exists("PersistentData\\Save_Data.txt"):
            pass
        
        # renaming a file can sometimes cause permission errors for a few frames, so keep trying until success
        while True:
            
            try:
                # open and get file data
                os.rename("PersistentData\\Save_Data.txt", "PersistentData\\Save_Data.saving")
                file = open("PersistentData\\Save_Data.saving", "r+")
                return file
            except:
                pass

def close_save_file(file:TextIOWrapper):
    file.close()
    os.rename("PersistentData\\Save_Data.saving", "PersistentData\\Save_Data.txt")

class Shop:

    def __init__(self, max_jars = 5, starting_jar_cost = 250, jar_price_hike_mult = 2, purchaseable_biomes:list[Biome] = []):
        
        # jar economy
        self.max_jars = max_jars
        self.starting_jar_cost = starting_jar_cost
        self.jar_price_hike_mult = jar_price_hike_mult

        # get data from the save file
        file = open_save_file()
        file_data = [line for line in file]
        close_save_file(file)
        
        # get the number of jars already purchased from the save file
        self.num_jars = int(file_data[1])

        # biome economy
        file_data = file_data[2:len(file_data)]

        # set the times purchased for the biomes to the save data's purchase values
        self.purchaseable_biomes = purchaseable_biomes
        for i in range(len(self.purchaseable_biomes)):
            self.purchaseable_biomes[i].times_purchased = int(file_data[i])

    def buy_jar(self) -> bool:

        # safely open the save file for reading and writing
        file:TextIOWrapper = open_save_file()

        # get the data from the file and wipe the file
        file_data = [line.strip() for line in file.readlines()]
        file.seek(0)
        file.truncate()
        
        # get the points and number of jars
        points = int(file_data[0])
        
        # current jar cost
        jar_cost = int(self.starting_jar_cost * (self.jar_price_hike_mult ** self.num_jars))

        # player has all the jars or is too broke to buy a jar
        if self.num_jars == self.max_jars or points < jar_cost:
            # unsuccessful purchase
            close_save_file()
            return False

        # spend the points
        points -= jar_cost
        file_data[0] = f"{points}\n"
        
        # add the jar
        self.num_jars += 1
        file_data[1] = self.num_jars

        # finalize the change
        for data in file_data:
            file.write(f"{data}\n")
        close_save_file(file)
        
        # successfully purchased
        return True

    def buy_biome(self, biome_index:int) -> bool:

        # safely open the save file for reading and writing
        file:TextIOWrapper = open_save_file()

        # get the data from the file and wipe the file
        file_data = [line.strip() for line in file.readlines()]
        file.seek(0)
        file.truncate()
        
        # get the points
        points = int(file_data[0])

        # player is too broke to buy this biome or the biome is maxed (obtains biome otherwise)
        if points < self.purchaseable_biomes[biome_index].get_price() or not self.purchaseable_biomes[biome_index].obtain():
            # unsuccessful purchase
            close_save_file()
            return False

        # spend the points
        points -= self.purchaseable_biomes[biome_index].get_price()
        file_data[0] = f"{points}\n"

        # save the biome purchase
        file_data[biome_index + 2] = f"{self.purchaseable_biomes[biome_index].times_purchased}\n"

        # finalize the change
        for data in file_data:
            file.write(f"{data}\n")
        close_save_file(file)
        
        # successfully purchased
        return True

    def close_shop(self):
        for biome in self.purchaseable_biomes:
            biome.close_biome()