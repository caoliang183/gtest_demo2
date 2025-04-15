// test/math_utils_test.cpp
#include <gtest/gtest.h>
#include <stdexcept>
#include "math_utils.hxx"

class MathUtilsTest : public ::testing::Test{
public:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(MathUtilsTest, AddTest){
    EXPECT_EQ(MathUtils::add(2, 3), 5);

}
TEST_F(MathUtilsTest, AddTest2){
    EXPECT_EQ(MathUtils::add(-2, 3), 1);

}
TEST_F(MathUtilsTest, AddTest3){
    EXPECT_EQ(MathUtils::add(0, 0), 0);

}

TEST_F(MathUtilsTest, SubtractTest){
    EXPECT_EQ(MathUtils::subtract(5, 3), 2);

}
TEST_F(MathUtilsTest, SubtractTest2){

    EXPECT_EQ(MathUtils::subtract(3, 5), -2);

}
TEST_F(MathUtilsTest, SubtractTest3){

    EXPECT_EQ(MathUtils::subtract(0, 0), 0);
    // 更多测试用例...
}

TEST_F(MathUtilsTest, MultiplyTest){
    EXPECT_EQ(MathUtils::multiply(2, 3), 6);

}
TEST_F(MathUtilsTest, MultiplyTest2){

    EXPECT_EQ(MathUtils::multiply(-2, 3), -6);

}
TEST_F(MathUtilsTest, MultiplyTest3){
    EXPECT_EQ(MathUtils::multiply(0, 5), 0);
    // 更多测试用例...
}

TEST_F(MathUtilsTest, DivideTest){
    EXPECT_DOUBLE_EQ(MathUtils::divide(6, 3), 2);

}
TEST_F(MathUtilsTest, DivideTest2){
    EXPECT_DOUBLE_EQ(MathUtils::divide(-6, 3), -2);

}    

// 改写为从 10 累加到 100 的批量化测试
TEST_F(MathUtilsTest, Batchtest) {
    for (int i = 10; i <= 100; ++i) {
        for (int j = 10; j <= 100; ++j) {
            int expected = i + j;
            int result = MathUtils::add(i, j);
            EXPECT_EQ(result, expected);
        }
    }
}
/*
// 存在中断的 gtest 测例
TEST_F(MathUtilsTest, SubtractInterruptionTest01) {
    int a = 10;
    int b = 5;
    if (a < b) {
        GTEST_FAIL() << "a is less than b, test interrupted";
    }
    int result = MathUtils::subtract(a, b);
    EXPECT_EQ(result, 5);
}

TEST_F(MathUtilsTest, SubtractInterruptionTest02) {
    int a = 20;
    int b = 20;
    if (a == b) {
        GTEST_FAIL() << "a is equal to b, test interrupted";
    }
    int result = MathUtils::subtract(a, b);
    EXPECT_EQ(result, 0);
}

TEST_F(MathUtilsTest, MultiplyInterruptionTest01) {
    int a = 0;
    int b = 5;
    if (a == 0) {
        GTEST_FAIL() << "a is zero, test interrupted";
    }
    int result = MathUtils::multiply(a, b);
    EXPECT_EQ(result, 0);
}

TEST_F(MathUtilsTest, MultiplyInterruptionTest02) {
    int a = 5;
    int b = 0;
    if (b == 0) {
        GTEST_FAIL() << "b is zero, test interrupted";
    }
    int result = MathUtils::multiply(a, b);
    EXPECT_EQ(result, 0);
}


// 3 个存在异常退出的 gtest 测例
TEST_F(MathUtilsTest, DivideExceptionTest1) {
    double a = 10.0;
    double b = 0.0;
    EXPECT_THROW(MathUtils::divide(a, b), std::invalid_argument);
}

TEST_F(MathUtilsTest, DivideExceptionTest2) {
    double a = 0.0;
    double b = 0.0;
    EXPECT_THROW(MathUtils::divide(a, b), std::invalid_argument);
}

TEST_F(MathUtilsTest, DivideExceptionTest3) {
    double a = -10.0;
    double b = 0.0;
    EXPECT_THROW(MathUtils::divide(a, b), std::invalid_argument);
}
*/