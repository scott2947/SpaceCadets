import urllib.request

emailID = input("Enter the email ID of the person's name wish to know >> ")
surname = emailID[len(emailID) - emailID[::-1].find("."):]
# print(surname)

page = urllib.request.urlopen("https://www.southampton.ac.uk/people?search_api_fulltext=" + surname + "&search_api_school=")
html = page.read()
webpage = html.decode("utf8")
page.close()

searchStr = "hidden md:block w-36 h-40 person-teaser__image mb-5 md:mb-0"

indices = []
i = 0
while i < len(webpage):
    j = webpage.find(searchStr, i)
    if j == -1:
        break
    indices.append(j)
    i = j + len(searchStr)
# print(indices)

found = False
i = 0
while not found and i < len(indices):
    j = indices[i] + len(searchStr)
    while webpage[j : j + 7] != "mailto:":
        j += 1
    k = j + 7
    emailID2 = ""
    while webpage[k] != "@":
        emailID2 += webpage[k]
        k += 1
    # print(emailID2)
    if emailID2 == emailID:
        x = indices[i] + len(searchStr) + 1
        while webpage[x] != '"':
            x += 1
        name = ""
        x += 1
        while webpage[x] != '"':
            name += webpage[x]
            x += 1
        print(name)
        found = True
    i += 1

# Solution will not work with old email addresses (search function does not work with old emails)
# Could change the urllib URL to search for names in the way given by the Space Cadets wiki