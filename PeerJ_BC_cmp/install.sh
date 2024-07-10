python3 -m pip uninstall Python-EasyGraph
rm -rf ./Easy-Graph
git clone --recursive https://github.com/yo123abxd/Easy-Graph.git

cp ./src/enable_warp_size/betweenness.cpp ./Easy-Graph/cpp_easygraph/functions/centrality/betweenness.cpp
cp ./src/enable_warp_size/centrality.cpp ./Easy-Graph/gpu_easygraph/functions/centrality/centrality.cpp
cp ./src/enable_warp_size/centrality.h ./Easy-Graph/cpp_easygraph/functions/centrality/centrality.h
cp ./src/enable_warp_size/cpp_easygraph.cpp ./Easy-Graph/cpp_easygraph/cpp_easygraph.cpp
cp ./src/enable_warp_size/gpu_easygraph.h ./Easy-Graph/gpu_easygraph/gpu_easygraph.h


if [ $# -eq 1 ]
then
    echo "using: " $1
    rm ./Easy-Graph/gpu_easygraph/functions/centrality/betweenness_centrality.cu
    cp $1 ./Easy-Graph/gpu_easygraph/functions/centrality/
else
    echo "using original"
fi


export EASYGRAPH_ENABLE_GPU="TRUE"
python3 -m pip install ./Easy-Graph


