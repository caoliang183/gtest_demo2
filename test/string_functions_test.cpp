#include <gtest/gtest.h>
#include "../include/string_functions.hxx"

// 字符串拼接函数的测试用例
TEST(StringFunctionsTest, ConcatenateTest){
    EXPECT_EQ(concatenate("Hello", " World"), "Hello World");
}

// 字符串长度函数的测试用例
TEST(StringFunctionsTest, StringLengthTest){
    EXPECT_EQ(stringLength("Hello"), 5);
}

// 字符串反转函数的测试用例
TEST(StringFunctionsTest, ReverseStringTest){
    EXPECT_EQ(reverseString("Hello"), "olleH");
}

// 检查字符串是否为空的测试用例
TEST(StringFunctionsTest, IsStringEmptyTestEmpty){
    EXPECT_TRUE(isStringEmpty(""));
}
