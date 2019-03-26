
def readPeopleList():
    peopleList = []
    for line in open('people','r'):
        peopleList.append(line.replace('\n',''))
    return peopleList

def addPeople(newPeople):
    file = open('people', 'a')
    file.write(newPeople + '\n')
    file.close()

def modPeople(oldPeople, newPeople):
    file_data = ""
    with open('people', 'r') as f:
        for line in f:
            if oldPeople in line:
                line = line.replace(oldPeople, newPeople)
            file_data += line
    with open('people', 'w') as f:
        f.write(file_data)

def delPeople(people):
    file_data = ""
    with open('people', 'r') as f:
        for line in f:
            if people in line:
                continue
            file_data += line
    with open('people', 'w') as f:
        f.write(file_data)

def readPartyMemberList():
    partyMemberList = []
    for line in open('partymember', 'r'):
        member = line.replace('\n', '').split("+++")
        partyMemberList.append(member)
    return partyMemberList

def addPartyMember(newMember):
    file = open('partymember', 'a')
    file.write(newMember + '\n')
    file.close()

def modPartyMember(oldPartyMember, newPartyMember):
    file_data = ""
    with open('partymember', 'r') as f:
        for line in f:
            if oldPartyMember in line:
                line = line.replace(oldPartyMember, newPartyMember)
            file_data += line
    with open('partymember', 'w') as f:
        f.write(file_data)

def delPartyMember(partyMember):
    file_data = ""
    with open('partymember', 'r') as f:
        for line in f:
            if partyMember in line:
                continue
            file_data += line
    with open('partymember', 'w') as f:
        f.write(file_data)
