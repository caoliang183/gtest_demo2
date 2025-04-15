#include <algorithm>
#include "../include/array_functions.hxx"
// 数组求和函数的实现
int sumArray(const std::vector<int>& arr) {
	int sum = 0;
	for (int num : arr) {
		sum += num;
	}
	return sum;
}


// 数组查找最大值函数的实现
int findMax(const std::vector<int>& arr) {
	int max = arr[0];
	for (int num : arr){
		if (num > max){
			max = num;
		}
	}
	return max;
}

// 数组查找最小值函数的实现
int findMin(const std::vector<int>& arr){
	int min = arr[0];
	for (int num : arr){
		if (num < min){
			min = num;
		}
	}
	return min;
}

// 数组排序函数的实现
std::vector<int> sortArray(const std::vector<int>& arr){
	
	std::vector<int> sorted = arr;
	std::sort(sorted.begin(), sorted.end());
	return sorted;
}