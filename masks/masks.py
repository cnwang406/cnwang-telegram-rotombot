from urllib3 import PoolManager,disable_warnings, exceptions
from datetime import datetime, timedelta

import math
import json
disable_warnings(exceptions.InsecureRequestWarning)
class MASKS():
    def __init__(self, pharmaciesUrl= r'https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json',home=[], maskChild=100,maskAdult=0, distance=10.0, maxCount=5):
        self.pharmaciesUrl = r'https://raw.githubusercontent.com/kiang/pharmacies/master/json/points.json'
        self.pharmaciesData=None
        #self.featurePharmacies=None
        self.home=home
        self.maskChild=maskChild
        self.maskAdult=maskAdult
        self.distance = distance
        self.maxCount=maxCount
        self.filteredPharmacies=None
        self.lastUpdate=None
        self.expireMinutes=15
    def setHome(self,loc): # in [longitude, latitude]
        self.home=loc
    def counts(self):
        return len(self.pharmaciesData) , len(self.filteredPharmacies)
    def getPharmaciesData(self,forceUpdate=False):
        if (self.lastUpdate != None and not forceUpdate)  :
            if self.lastUpdate+timedelta(minutes=self.expireMinutes)>datetime.today():
                #print (f'lastupdate {self.lastUpdate} + {self.expireMinutes}mins = {self.lastUpdate+timedelta(minutes=self.expireMinutes)}, > {datetime.today()}, skip')
                return
        
        http = PoolManager()
        r = http.request('GET', self.pharmaciesUrl)
        allData = json.loads(r.data)['features']
        self.pharmaciesData = []
        for phd in allData:
            data = {}
            geo = phd['geometry']['coordinates']
            name = phd['properties']['name']
            address = phd['properties']['address']
            mask_adult = phd['properties']['mask_adult']
            mask_child = phd['properties']['mask_child']
            available = phd['properties']['available']
            note = phd['properties']['note']
            data = {
                'name': name,
                'address': address,
                'mask_adult': mask_adult,
                'mask_child': mask_child,
                'available': available,
                'note': note,
                'geometry': geo
            }
            self.pharmaciesData.append(data)
        self.lastUpdate =datetime.today()
    def geoDistance(self,loc1, loc2):

        R = 6373.0
        #radius of the Earth
        lat1 = math.radians(loc1[1])
        lon1 = math.radians(loc1[0])
        lat2 = math.radians(loc2[1])
        lon2 = math.radians(loc2[0])

        dlon = lon2 - lon1
        #change in coordinates
        dlat = lat2 - lat1

        a = math.sin(
            dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        #Haversine formula
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

    def filterOut(self):
        #print (f'start to filter, withwin {self.distance}km, child>={self.maskChild}, adult>={self.maskAdult}, for first {self.maxCount} pharmacies, center at {self.home}')
        hits = []
        #hitsCount = 0
        for phd in self.pharmaciesData:
            phdDistance = self.geoDistance(self.home, phd['geometry'])
            #print (f'{phdDistance}km, away from {phd["geometry"]}, {phd["mask_child"]}/{phd["mask_adult"]}' )
            if phdDistance <= self.distance:
                
                if (phd['mask_adult'] >= self.maskAdult and phd['mask_child'] >= self.maskChild):
                    phd['distance'] = phdDistance

                    hits.append(phd)
        hits = sorted(hits, key=lambda i: (i['distance']))
        hits = hits[:self.maxCount]
        self.filteredPharmacies=hits
        return
 
    def numberToEmoji(self,n):
        emojis = [
            '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'
        ]
        ss = str(n)
        ret = ''
        for s in ss:
            ret += emojis[int(s)]
        return ret


    def filteredS(self):
        output = f'start to filter, withwin {self.distance}km, child>={self.maskChild}, adult>={self.maskAdult}, for first {self.maxCount} pharmacies, center at {self.home})'
        output += f'\nmeet criteria {len(self.filteredPharmacies)} out of {len(self.pharmaciesData)} pharmacies \n\n'
        if len(self.filteredPharmacies) == 0:
            output += '\n 🈚️🈚️🈚️ NO FOUND 🈚️🈚️🈚️'
        for hit in self.filteredPharmacies:
            output+=self.record2Str(hit)
            #if hit["mask_child"] > 200:
            #    headings = '‼️'
            #else:
            #    headings = ''
            #output += f'{headings}💊{hit["name"]} 童🧒🏻 {self.numberToEmoji(hit["mask_child"])}/ 大👩🏻 {hit["mask_adult"]} ({hit["distance"]:.2f}km) {headings}\n'
            #output += f'{hit["address"]} {hit["note"]}\n'
            output += '\n'
        output += f'---[FINISHED]---\n(updated {datetime.strftime(self.lastUpdate,"%y-%m-%d %H:%M:%S")})'
        return output

    def findMasks(self, loc=None,child=None, adult=None, distance=None, maxcount=None, sortKey='distance'):
        self.home = loc if loc else self.home
        self.maskChild = child if child is not None else self.maskChild
        self.maskAdult = adult if adult is not None else self.maskAdult
        self.distance = distance if distance is not None else self.distance
        self.maxCount  = maxcount if maxcount is not None else self.maxCount            
        self.getPharmaciesData()
        self.filterOut()  
        key='distance'
        reverse=False        # default distance small to large  
        if sortKey[0]=='-':
            reverse = True
            sortKey=sortKey[1:]
        if sortKey[0].isupper():
            reverse=True
        
        if sortKey.lower() in ('d','distance', 'dist'):
            key='distance'
        if sortKey.lower() in ('c','child_mask','mask_child','child','childmask'):
            key='mask_child'
        if sortKey.lower() in ('a','adult_mask','mask_adult','adult','adultmask'):
            key='mask_adult'
        
        self.filteredPharmacies = sorted(self.filteredPharmacies, key=lambda i: (i[key]),reverse=reverse)
        return self.filteredPharmacies
    def defs(self):
        print (f'{self.home},{self.maskChild},{self.maskAdult}, {self.distance }km, {self.maxCount}')
    
    def record2Str(self,hit ):
        #hit=self.filteredPharmacies[idx]
        output=''
        if hit["mask_child"] > 200:
                headings = '‼️'
        else:
                headings = ''
        output += f'{headings}💊{hit["name"]} 童🧒🏻 {self.numberToEmoji(hit["mask_child"])}/ 大👩🏻 {hit["mask_adult"]} ({hit["distance"]:.2f}km) {headings}\n'
        output += f'{hit["address"]} {hit["note"]}'
        return output

    def recordn2Str(self,idx ):
        hit=self.filteredPharmacies[idx]
        output=''
        if hit["mask_child"] > 200:
                headings = '‼️'
        else:
                headings = ''
        output += f'{headings}💊{hit["name"]} 童🧒🏻 {self.numberToEmoji(hit["mask_child"])}/ 大👩🏻 {hit["mask_adult"]} ({hit["distance"]:.2f}km) {headings}\n'
        output += f'{hit["address"]} {hit["note"]}'
        return output
    def recordn2StrShort(self,idx ):
        hit=self.filteredPharmacies[idx]
        output=''
        output += f'{hit["name"]} 童🧒🏻 {self.numberToEmoji(hit["mask_child"])}/ 大👩🏻 {hit["mask_adult"]} ({hit["distance"]:.2f}km)\n'
        return output
