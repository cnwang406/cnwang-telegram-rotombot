from masks.masks import MASKS
from time import sleep

masks=MASKS(home=[121.0185, 24.833318])

#masks.getPharmaciesData()
#masks.filterOut()
#print (masks.counts ())
#sleep (1)
#masks.getPharmaciesData()
#masks.filterOut()
#print(masks.filteredS())
masks.defs()
masks.findMasks(loc=[120.2911, 22.79612], child=0,distance=5.0, sortKey='d')
print(masks.filteredPharmacies[0])
#print (masks.filteredS())
masks.defs()