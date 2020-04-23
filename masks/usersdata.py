import psycopg2
import sys
from datetime import datetime


class Users():
    def __init__(self, database, user, password, host):
        self.con = None
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.dbConn()
        if self.con is None:
            print('connect Fail')
        else:
            print('connect ok')
        # self.users=[]

    def dbConn(self):
        con = psycopg2.connect(
            host=self.host, database=self.database, user=self.user, password=self.password)
        self.con = con
        return self.con

    # user = {'name': string, 'loc':[lon, lat], 'child':int, 'adult':int, 'distance':float, 'maxcount':int}

    def newUser(self, name, id=111, loc=[0, 0], child=100, adult=0, distance=5.0, maxcount=5, count=1):
        self.con = self.dbConn()
        ck = self.checkUser(name)
        if ck:
            count = ck[8]
            print(
                f'user {name} already exist, use {count} times ({type(count)}), last is {ck[9]} replace!')

            sqlStr = f"""UPDATE users SET loc_lon ='{loc[0]}' , 
                    loc_lat='{loc[1]}', child='{child}', adult='{adult}', maxcount='{maxcount}', distance='{distance}', update='{datetime.today()}'
                    WHERE username='{name}'"""
        else:
            sqlStr = f"""INSERT INTO users (userid,username, loc_lon, loc_lat, child, adult, maxcount, distance, count, update) VALUES
                        ('{id}','{name}','{loc[0]}','{loc[1]}','{child}','{adult}','{maxcount}','{distance}','{count}', '{datetime.today()}')
            """

        ret = self.executeSql(sqlStr)

        tmp = {'name': name, 'loc': loc, 'child': child,
               'adult': adult, 'distance': distance, 'maxcount': maxcount}
        return ret

    def userAccess(self, name):
        sqlStr = f"""SELECT username, count, update FROM users WHERE username = '{name}'"""
        try:
            self.con = self.dbConn()
            cur = self.con.cursor()
            cur.execute(sqlStr)
            ret = cur.fetchone()
            if ret is None:
                self.newUser(name)
        except psycopg2.DatabaseError as e:
            print(f'error at useraccess {e}')
            return False
        finally:
            if ret is None:
                count = 0
            else:
                count = int(ret[1])+1
            sqlStr = f"""UPDATE users SET count={count}, update='{datetime.today()}'
                    WHERE username='{name}'"""
            self.executeSql(sqlStr)
            pass
        return f'{name} {count} {datetime.today()}'

    def executeSql(self, sqlStr):
        self.con = self.dbConn()
        success = True
        try:
            cur = self.con.cursor()
            cur.execute(sqlStr)
            self.con.commit()
        except psycopg2.DatabaseError as e:
            self.con.rollback()
            print(e.pgerror)
            success = False
        finally:
            if self.con:
                self.con.close()
            print(f'sqlstr=[{sqlStr}] done!')
        return success

    def checkUser(self, lookingFor):
        sqlStr = f"SELECT userid, username, loc_lon, loc_lat, child, adult, maxcount, distance, count, update FROM users WHERE username='{lookingFor}'"
        self.con = self.dbConn()
        cur = self.con.cursor()
        cur.execute(sqlStr)
        ret = cur.fetchone()
        print(f'return ={ret}, type={type(ret)}')
        self.con.close()
        if ret:
            return ret
        else:
            return False
        """
        for user in self.username:
            if user['name'] == lookingFor:
                return True
        return False
        """

    def getUserLoc(self, lookingFor):
        sqlStr = f"SELECT loc_lon,loc_lat FROM users WHERE username='{lookingFor}"
        self.con = self.dbConn()
        cur = self.con.cursor()
        cur.execute(sqlStr)
        ret = cur.fetchone()

        self.con.close()
        if ret is not None:
            return [ret[0], ret[1]]
        else:
            return None
        """
        for user in self.users:
            if user['name'] == lookingFor:
                return user['loc']
        return None
        """

    def getUserSetting(self, lookingFor):
        sqlStr = f"SELECT username, loc_lon, loc_lat, child, adult, maxcount, distance FROM users WHERE username='{lookingFor}"
        self.con = self.dbConn()
        cur = con.cursor()
        cur.execute(sqlStr)
        ret = cur.fetchone()
        print(ret)
        if ret is not None:
            return [ret[0], ret[1]]
        else:
            return None
        """
            for user in self.users:
                if user['name'] == lookingFor:
                    return user
            return None
        """
    """
    def addUser(self, newUser):
        if self.checkUser(newUser['name']):
            return False    # exist
        else:
            self.users.append(newUser)
            return True
    """

    def modifyUserLoc(self, name, loc):
        sqlStr = f"""UPDATE users SET loc_lon ='{loc[0]}' , 
                    loc_lat='{loc[1]}' WHERE username='{name}'"""
        ret = self.executeSql(sqlStr)
        if ret:
            print('update OK')
        else:
            print('update Fail')
        return ret
        """            
        for user in self.users:
            if user['name'] == name:
                user['loc'] = loc
            return True
        return False
        """

    def modifyUserSetting(self, name, loc=[0, 0], child=100, adult=0, distance=5.0, maxcount=5):
        sqlStr = f"""UPDATE users SET loc_lon ='{loc[0]}' , 
                    loc_lat='{loc[1]}', child='{child}', adult='{adult}', maxcount='{maxcount}', distance='{distance}'
                    WHERE username='{name}'"""
        ret = self.executeSql(sqlStr)
        if ret:
            print('update OK')
        else:
            print('update Fail')
        return ret
        """
        for user in self.users:
            if user['name'] == name:
                user['loc'] = loc
                user['child']=child
                user['adult']=adult
                user['distance']=distance
                user['maxcount']=maxcount
                return True
        return False
        """

    def addModUserLoc(self, modifyUser, userid):
        self.newUser(name=modifyUser['name'], id=userid, loc=modifyUser['loc'], child=modifyUser['child'], adult=modifyUser['adult'],
                     distance=modifyUser['dist'], maxcount=modifyUser['maxcount'])
        """
        print (modifyUser)
        for user in self.users:
            if user['name'] == modifyUser['name']:
                user=modifyUser
            return
        #not found
        self.addUser(modifyUser)
        """

    def dump(self):
        self.con = self.dbConn()
        sqlStr = "SELECT id, username, loc_lon, loc_lat, child, adult, maxcount, distance, count, update FROM users"
        try:
            cur = self.con.cursor()
            cur.execute(sqlStr)
            ret = cur.fetchall()
            pass
        except psycopg2.DatabaseError as e:
            print('dump fail' + e)
            return False
            pass
        finally:
            if self.con:
                self.con.close()
        output = []
        for c in ret:
            output.append(list(c))
        return output

    def dumps(self):
        output = self.dump()
        ret = '-'*10+'\n'
        for user in output:
            ret += f'{user[1]} @ [{user[2]},{user[3]}] child:{user[4]}, adult:{user[5]}, dist:{user[6]}, maxcount:{user[7]}, use {user[8]}, last is {user[9]}\n'
        return ret
