#include <gtest/gtest.h>
#include <vector>
#include "../include/array_functions.hxx"

// 数组求和函数的测试用例

TEST(ArrayFunctionsTest, SumArrayTest){
	std::vector<int> arr = { 1, 1 };
	EXPECT_EQ(sumArray(arr), 2);
}
TEST(ArrayFunctionsTest, SumArrayTest2){
	std::vector<int> arr = { 1, 2 };
	EXPECT_EQ(sumArray(arr), 3);
}
TEST(ArrayFunctionsTest, SumArrayTest3){
	std::vector<int> arr = { 1, 3 };
	EXPECT_EQ(sumArray(arr), 4);
}
TEST(ArrayFunctionsTest, SumArrayTest4){
	std::vector<int> arr = { 1, 4 };
	EXPECT_EQ(sumArray(arr), 5);
}
TEST(ArrayFunctionsTest, SumArrayTest5){
	std::vector<int> arr = { 1, 5 };
	EXPECT_EQ(sumArray(arr), 6);
}
TEST(ArrayFunctionsTest, SumArrayTest6){
	std::vector<int> arr = { 1,6 };
	EXPECT_EQ(sumArray(arr), 7);
}
TEST(ArrayFunctionsTest, SumArrayTest7){
	std::vector<int> arr = { 1, 7 };
	EXPECT_EQ(sumArray(arr), 8);
}
TEST(ArrayFunctionsTest, SumArrayTest8){
	std::vector<int> arr = { 1, 8 };
	EXPECT_EQ(sumArray(arr), 9);
}
TEST(ArrayFunctionsTest, SumArrayTest9){
	std::vector<int> arr = { 1, 9 };
	EXPECT_EQ(sumArray(arr), 10);
}
TEST(ArrayFunctionsTest, SumArrayTest10){
	std::vector<int> arr = { 1, 2, 3};
	EXPECT_EQ(sumArray(arr), 6);
}
TEST(ArrayFunctionsTest, SumArrayTest11){
	std::vector<int> arr = { 1, 2, 4 };
	EXPECT_EQ(sumArray(arr), 7);
}
TEST(ArrayFunctionsTest, SumArrayTest12){
	std::vector<int> arr = { 1, 2, 5 };
	EXPECT_EQ(sumArray(arr), 8);
}
TEST(ArrayFunctionsTest, SumArrayTest13){
	std::vector<int> arr = { 1, 2, 6 };
	EXPECT_EQ(sumArray(arr), 9);
}
TEST(ArrayFunctionsTest, SumArrayTest14){
	std::vector<int> arr = { 1, 2, 7 };
	EXPECT_EQ(sumArray(arr), 10);
}
TEST(ArrayFunctionsTest, SumArrayTest15){
	std::vector<int> arr = { 1, 2, 8 };
	EXPECT_EQ(sumArray(arr), 11);
}
TEST(ArrayFunctionsTest, SumArrayTest16){
	std::vector<int> arr = { 1, 2, 9 };
	EXPECT_EQ(sumArray(arr), 112);
}
TEST(ArrayFunctionsTest, SumArrayTest17){
	std::vector<int> arr = { 1, 2, 3, 4 };
	EXPECT_EQ(sumArray(arr), 10);
}
TEST(ArrayFunctionsTest, SumArrayTest18){
	std::vector<int> arr = { 1, 2, 3, 5 };
	EXPECT_EQ(sumArray(arr), 11);
}
TEST(ArrayFunctionsTest, SumArrayTest19){
	std::vector<int> arr = { 1, 2, 3, 6 };
	EXPECT_EQ(sumArray(arr), 12);
}
TEST(ArrayFunctionsTest, SumArrayTest20){
	std::vector<int> arr = { 1, 2, 3, 7 };
	EXPECT_EQ(sumArray(arr), 13);
}

// 数组查找最大值函数的测试用例
TEST(ArrayFunctionsTest, FindMaxTest){
	std::vector<int> arr = { 1, 2};
	EXPECT_EQ(findMax(arr), 2);
}
TEST(ArrayFunctionsTest, FindMaxTest2){
	std::vector<int> arr = { 1, 2, 3 };
	EXPECT_EQ(findMax(arr), 3);
}
TEST(ArrayFunctionsTest, FindMaxTest3){
	std::vector<int> arr = { 1, 2, 3, 4 };
	EXPECT_EQ(findMax(arr), 4);
}
TEST(ArrayFunctionsTest, FindMaxTest4){
	std::vector<int> arr = { 1, 2, 3, 4, 5 };
	EXPECT_EQ(findMax(arr), 5);
}
TEST(ArrayFunctionsTest, FindMaxTest5){
	std::vector<int> arr = { 1, 2, 3, 4, 5, 6 };
	EXPECT_EQ(findMax(arr), 6);
}

// 数组查找最小值函数的测试用例
TEST(ArrayFunctionsTest, FindMinTest){
	std::vector<int> arr = { 1, 2, 3, 4, 5 };
	EXPECT_EQ(findMin(arr), 1);
}
TEST(ArrayFunctionsTest, FindMinTest2){
	std::vector<int> arr = { 2, 3, 4, 5 };
	EXPECT_EQ(findMin(arr), 2);
}
TEST(ArrayFunctionsTest, FindMinTest3){
	std::vector<int> arr = { 3, 4, 5 };
	EXPECT_EQ(findMin(arr), 3);
}
TEST(ArrayFunctionsTest, FindMinTest4){
	std::vector<int> arr = { 4, 5 };
	EXPECT_EQ(findMin(arr), 4);
}
TEST(ArrayFunctionsTest, FindMinTest5){
	std::vector<int> arr = { 5,6,7 };
	EXPECT_EQ(findMin(arr), 5);
}

// 数组排序函数的测试用例
TEST(ArrayFunctionsTest, SortArrayTest){
	std::vector<int> arr = { 5, 4, 3, 2, 1 };
	std::vector<int> sorted = { 1, 2, 3, 4, 5 };
	EXPECT_EQ(sortArray(arr), sorted);
}