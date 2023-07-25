def write_log(a):
    with open('./log.txt','w') as f:
        f.write(str(a))
        f.close()