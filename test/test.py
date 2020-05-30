import random
import datetime
import time

# noupdate=True
# c=0
# while True:
#
#     now_time = datetime.datetime.now()
#     now_minute = now_time.second
#     change_minute = 0
#     cha = 28 - now_minute
#     if noupdate and (0 < cha < 10):
#         sleeptime = random.uniform(cha - 0.16,cha + 0.18)
#     elif noupdate and cha<=0:
#         sleeptime = random.uniform(0.51, 0.62)
#         c+=1
#     else:
#         sleeptime = random.uniform(8.2, 9.5)
#         c = 0
#         if (now_minute >= 40):
#             noupdate = True
#
#     if c==3:
#         noupdate=False
#     print(noupdate)
#     print(str(now_time)+'  '+str(sleeptime))
#     time.sleep(sleeptime)

# n=[3]
#
# def a(n):
#     n.append(1)
# print(n)
# log_file_path = 'log\\' + str(datetime.datetime.now().date()) + '.txt'
# f=open(log_file_path,'a',encoding='utf-8')
# f.write('test'+'\n')
# f.close()


f = open("course.txt", 'r', encoding='utf-8')
di=eval(f.read())
print(di)