import mechanize

browser = mechanize.Browser()
browser.set_handle_robots(False)

url = 'http://localhost:8515'
link_text = 'Connect with Instagram'

r = browser.open(url)
browser.find_link(text=link_text)
req = browser.click_link(text=link_text)
browser.open(req)

f = open('workfile', 'w')
f.write(browser.response().read())

#print browser.response().read()

browser.select_form(nr=0)
browser.form['username'] = 'username'
browser.form['password'] = 'password'
browser.submit(nr=0)

#formcount = 0
#for frm in browser.forms():  
#  if str(frm.attrs["id"]) == "login-form":
#    break
#  formcount = formcount + 1
#browser.select_form(nr=formcount)

#r = browser.open('http://localhost:8515')

#for link in browser.links():
#    print(link)
#    print(link.url)

#browser.follow_link(link)
#print(browser.geturl())
