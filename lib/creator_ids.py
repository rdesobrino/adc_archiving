import random

def make_random_id():

    id = ""
    for i in range(16):
        id += str(random.randint(0,9))
    return id

print(make_random_id())

#U8ZTVPfTxTAJgyNGv51iFd2dr7XT6a attribute id
# 6990252230437624 contact id