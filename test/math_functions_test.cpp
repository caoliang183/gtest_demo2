#include <gtest/gtest.h>
#include "../include/math_functions.hxx"

// 加法函数的测试用例
TEST(MathFunctionsTest, AddTestPositive){
    EXPECT_EQ(add(2, 3), 5);
}

TEST(MathFunctionsTest, AddTestNegative){
    EXPECT_EQ(add(-2, -3), -5);
}

TEST(MathFunctionsTest, AddTestMixed){
    EXPECT_EQ(add(2, -3), -1);
}

// 减法函数的测试用例
TEST(MathFunctionsTest, SubtractTestPositive){
    EXPECT_EQ(subtract(5, 3), 2);
}

TEST(MathFunctionsTest, SubtractTestNegative){
    EXPECT_EQ(subtract(-5, -3), -2);
}

TEST(MathFunctionsTest, SubtractTestMixed){
    EXPECT_EQ(subtract(5, -3), 8);
}

// 乘法函数的测试用例
TEST(MathFunctionsTest, MultiplyTestPositive){
    EXPECT_EQ(multiply(2, 3), 6);
}

TEST(MathFunctionsTest, MultiplyTestNegative){
    EXPECT_EQ(multiply(-2, -3), 6);
}

TEST(MathFunctionsTest, MultiplyTestMixed){
    EXPECT_EQ(multiply(2, -3), -6);
}

// 除法函数的测试用例
TEST(MathFunctionsTest, DivideTestPositive){
    EXPECT_EQ(divide(6, 3), 2);
}

TEST(MathFunctionsTest, DivideTestNegative){
    EXPECT_EQ(divide(-6, -3), 2);
}

TEST(MathFunctionsTest, DivideTestMixed){
    EXPECT_EQ(divide(6, -3), -2);
}

TEST(MathFunctionsTest, DivideByZero){
    EXPECT_THROW(divide(6, 0), std::runtime_error);
}

// 取模函数的测试用例
TEST(MathFunctionsTest, ModuloTestPositive){
    EXPECT_EQ(modulo(7, 3), 1);
}

TEST(MathFunctionsTest, ModuloTestNegative){
    EXPECT_EQ(modulo(-7, -3), -1);
}

TEST(MathFunctionsTest, ModuloTestMixed){
    EXPECT_EQ(modulo(7, -3), 1);
}

TEST(MathFunctionsTest, ModuloByZero){
    EXPECT_THROW(modulo(7, 0), std::runtime_error);
}