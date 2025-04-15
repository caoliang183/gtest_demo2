// src/vector_utils.cpp
#include <numeric>
#include "vector_utils.hxx"

int VectorUtils::sum(const std::vector<int>& vec){
	
    return std::accumulate(vec.begin(), vec.end(), 0);
}

double VectorUtils::average(const std::vector<int>& vec){
	
    return static_cast<double>(sum(vec)) / vec.size();
}

bool VectorUtils::contains(const std::vector<int>& vec, int value){
	
    return std::find(vec.begin(), vec.end(), value) != vec.end();
}    