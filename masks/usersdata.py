class Users():
    def __init__(self):
        self.users=[]

    # user = {'name': string, 'loc':[lon, lat], 'child':int, 'adult':int, 'distance':float, 'maxcount':int}
    def newUser(self, name, loc=[0,0],child=100, adult=0, distance=5.0, maxcount=5):
        tmp={'name':name, 'loc':loc, 'child':child, 'adult':adult, 'distance':distance, 'maxcount':maxcount}
        return tmp
    def checkUser(self, lookingFor):
        for user in self.users:
            if user['name'] == lookingFor:
                return True
        return False
    def getUserLoc(self, lookingFor):
        for user in self.users:
            if user['name'] == lookingFor:
                return user['loc']
        return None
    
    def getUserSetting(self, lookingFor):
            for user in self.users:
                if user['name'] == lookingFor:
                    return user
            return None

    def addUser(self, newUser):
        if self.checkUser(newUser['name']):
            return False    # exist
        else:
            self.users.append(newUser)
            return True

    def modifyUserLoc(self,name, loc):
        for user in self.users:
            if user['name'] == name:
                user['loc'] = loc
            return True
        return False
    def modifyUserSetting(self, name, loc=[0,0],child=100, adult=0, distance=5.0, maxcount=5):
        for user in self.users:
            if user['name'] == name:
                user['loc'] = loc
                user['child']=child
                user['adult']=adult
                user['distance']=distance
                user['maxcount']=maxcount
                return True
        return False

    def addModUserLoc(self,modifyUser):
        print (modifyUser)
        for user in self.users:
            if user['name'] == modifyUser['name']:
                user=modifyUser
            return
        #not found
        self.addUser(modifyUser)
        
    def dump(self):
        print (self.users)
        return (len(self.users))

    def dumps(self):
        ret='-'*10+'\n'
        for user in self.users:
            ret+=f'{user["name"]} @ [{user["loc"]}, child:{user["child"]}, adult:{user["adult"]}, dist:{user["distance"]}, maxcount:{user["maxcount"]}\n'
        return ret

        