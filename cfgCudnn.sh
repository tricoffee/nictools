cp include/cudnn.h /usr/local/cuda/include/
cp lib64/libcudnn* /usr/local/cuda/lib64/
chmod a+r /usr/local/cuda/include/cudnn.h
chmod a+r /usr/local/cuda/lib64/libcudnn*
rm -rf libcudnn.so libcudnn.so.7
ln -s libcudnn.so.7.6.3 libcudnn.so.7
ln -s libcudnn.so.7 libcudnn.so
cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2