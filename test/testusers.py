import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from masks.usersdata import Users

DB_USER=os.environ.get('DB_USER')
DB_USERPASSWORD=os.environ.get('DB_PASSWORD')
DB_DATABASE=os.environ.get('DB_DATABASE')
DB_HOST=os.environ.get('DB_HOST')


users=Users(database=DB_DATABASE,user=DB_USER,password=DB_USERPASSWORD,host=DB_HOST)


print (users.dump())
a=users.newUser('aaa',111)
#print ('check',users.checkUser(a['name']))
print ('add user aaa...')
print ('adduser aaa', users.newUser(name='aaa', loc=[10,10]))
print ('adduser bbb',(users.newUser(name='bbb', loc=[120.99778, 24.776377],child=0,adult=0,distance=10.0,maxcount=5)))
print ('adduser ccc',(users.newUser(name='ccc', loc=[120.99778, 24.776377],child=100,adult=100,distance=1.0,maxcount=10)))

print (users.dump())
print ('check',users.checkUser('aaa'))
print ('modify aaa', users.modifyUserLoc(name='aaa', loc=[119.99778, 25.776377]))
print (users.dump())
print ('modify ddd',users.modifyUserSetting(name='ddd',child=200))
print (users.dumps())
