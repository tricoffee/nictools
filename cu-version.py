import os
os.system('cat /usr/local/cuda/version.txt')
#os.system('whereis cudnn')
try:
    head_file = open('/usr/local/cuda/include/cudnn.h')
except:
    head_file = open('/usr/include/cudnn.h')
lines = head_file.readlines()
for line in lines:
    line = line.strip()
    if line.startswith('#define CUDNN_MAJOR'):
        line = line.split('#define CUDNN_MAJOR')
        n1 = int(line[1])
        continue
    if line.startswith('#define CUDNN_MINOR'):
        line = line.split('#define CUDNN_MINOR')
        n2 = int(line[1])
        continue
    if line.startswith('#define CUDNN_PATCHLEVEL'):
        line = line.split('#define CUDNN_PATCHLEVEL')
        n3 = int(line[1])
        break
print('CUDNN Version ', str(n1)+'.'+str(n2)+'.'+str(n3))
#CUDA Version 10.0.130
# CUDNN Version  7.4.2