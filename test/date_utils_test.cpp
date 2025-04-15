// test/date_utils_test.cpp
#include <gtest/gtest.h>
#include "date_utils.hxx"

class DateUtilsTest : public ::testing::Test {
public:
	void SetUp() override {}
	void TearDown() override {}
};

TEST_F(DateUtilsTest, IsLeapYearTest) {
	EXPECT_TRUE(DateUtils::isLeapYear(2020));
	
}
TEST_F(DateUtilsTest, IsLeapYearTest2) {
	
	EXPECT_TRUE(DateUtils::isLeapYear(2000));
	
}
TEST_F(DateUtilsTest, IsLeapYearTest3) {
	EXPECT_TRUE(DateUtils::isLeapYear(1980));
	
}
TEST_F(DateUtilsTest, IsLeapYearTest4) {
	EXPECT_TRUE(DateUtils::isLeapYear(1960));
	
}
TEST_F(DateUtilsTest, IsLeapYearTest5) {
	EXPECT_TRUE(DateUtils::isLeapYear(1940));
	
}

TEST_F(DateUtilsTest, DaysInMonthTest) {
	EXPECT_EQ(DateUtils::daysInMonth(2020, 2), 29);
	
}
TEST_F(DateUtilsTest, DaysInMonthTest2) {
	EXPECT_EQ(DateUtils::daysInMonth(2021, 2), 28);
	
}
TEST_F(DateUtilsTest, DaysInMonthTest3) {
	EXPECT_EQ(DateUtils::daysInMonth(2021, 1), 31);
	
}
TEST_F(DateUtilsTest, DaysInMonthTest4) {
	EXPECT_EQ(DateUtils::daysInMonth(2021, 4), 30);

}
TEST_F(DateUtilsTest, DaysInMonthTest5) {

	EXPECT_EQ(DateUtils::daysInMonth(2021, 6), 30);
	// 更多测试用例...
}