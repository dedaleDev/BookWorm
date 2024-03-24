
str1 = "Harry Potter"
str2 = "Hary Poter and the Philosopher's Stone"

def compare(str1, str2)->bool:
    str1 = str1.lower()
    str2 = str2.lower()
    if str1.replace(" ", "") in str2.replace(" ", ""):
        print('phase 1')
        return True
    else:
        str1 = str1.split(" ")
        str2 = str2.split(" ")
        for word in str1:
                if word in str2:
                    print('phase 2', word)
                    return True
        return False

    

print(compare(str1,str2))