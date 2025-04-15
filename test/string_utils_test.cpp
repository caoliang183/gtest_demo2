// test/string_utils_test.cpp
#include <gtest/gtest.h>
#include "string_utils.hxx"

class StringUtilsTest : public ::testing::Test{
public:
    void SetUp() override {}
    void TearDown() override {}
};

TEST_F(StringUtilsTest, ToUpperCaseTest){
    EXPECT_EQ(StringUtils::toUpperCase("hello"), "HELLO");

}
TEST_F(StringUtilsTest, ToUpperCaseTest2){

    EXPECT_EQ(StringUtils::toUpperCase("Hello"), "HELLO");

}
TEST_F(StringUtilsTest, ToUpperCaseTest3){

    EXPECT_EQ(StringUtils::toUpperCase("123abc"), "123ABC");
    // 更多测试用例...
}

TEST_F(StringUtilsTest, ToLowerCaseTest){
    EXPECT_EQ(StringUtils::toLowerCase("HELLO"), "hello");

}
TEST_F(StringUtilsTest, ToLowerCaseTest2){

    EXPECT_EQ(StringUtils::toLowerCase("Hello"), "hello");

}
TEST_F(StringUtilsTest, ToLowerCaseTest3){

    EXPECT_EQ(StringUtils::toLowerCase("123ABC"), "123abc");
    // 更多测试用例...
}

TEST_F(StringUtilsTest, StartsWithTest){
    EXPECT_TRUE(StringUtils::startsWith("hello world", "hello"));

}
TEST_F(StringUtilsTest, StartsWithTest2){

    EXPECT_TRUE(StringUtils::startsWith("abc", "a"));
    // 更多测试用例...
}

TEST_F(StringUtilsTest, EndsWithTest){
    EXPECT_TRUE(StringUtils::endsWith("hello world", "world"));

}   
TEST_F(StringUtilsTest, EndsWithTest2){

    EXPECT_TRUE(StringUtils::endsWith("abc", "c"));
    // 更多测试用例...
}    