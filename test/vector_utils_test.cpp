// test/vector_utils_test.cpp
#include <gtest/gtest.h>
#include "vector_utils.hxx"
#include <vector>

class VectorUtilsTest : public ::testing::Test{
protected:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(VectorUtilsTest, SumTest){
    std::vector<int> vec = {1, 2, 3, 4, 5};
    EXPECT_EQ(VectorUtils::sum(vec), 15);

    // 更多测试用例...
}

TEST_F(VectorUtilsTest, AverageTest){
    std::vector<int> vec = {1, 2, 3, 4, 5};
    EXPECT_DOUBLE_EQ(VectorUtils::average(vec), 3);

    // 更多测试用例...
}

TEST_F(VectorUtilsTest, ContainsTest){
    std::vector<int> vec = {1, 2, 3, 4, 5};
    EXPECT_TRUE(VectorUtils::contains(vec, 3));
    // 更多测试用例...
}    