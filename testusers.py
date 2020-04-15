from masks.usersdata import Users


users = Users()

print (users.dump())
a=users.newUser('aaa')
print ('check',users.checkUser(a['name']))
print ('add user aaa...')
print ('adduser aaa', users.addUser(users.newUser(name='aaa', loc=[10,10])))
print ('adduser bbb',users.addUser(users.newUser(name='bbb', loc=[120.99778, 24.776377],child=0,adult=0,distance=10.0,maxcount=5)))
print ('adduser ccc',users.addUser(users.newUser(name='ccc', loc=[120.99778, 24.776377],child=100,adult=100,distance=1.0,maxcount=10)))

print (users.dump())
print ('check',users.checkUser('aaa'))
print ('modify aaa', users.modifyUserLoc(name='aaa', loc=[119.99778, 25.776377]))
print (users.dump())
print ('modify ddd',users.modifyUserSetting(name='ddd',child=200))
print (users.dump())
