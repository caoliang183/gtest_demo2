// main.cpp
#include <gtest/gtest.h>
#include <iostream>
#include "math_utils.hxx"
#include "string_utils.hxx"
#include "vector_utils.hxx"
#include "date_utils.hxx"

int main(int argc, char **argv) {
	std::cout << "MathUtils::add(2, 3) = " << MathUtils::add(2, 3) << std::endl;
	std::cout << "StringUtils::toUpperCase(\"hello\") = " << StringUtils::toUpperCase("hello") << std::endl;
	std::vector<int> vec = {1, 2, 3, 4, 5};
	std::cout << "VectorUtils::sum(vec) = " << VectorUtils::sum(vec) << std::endl;
	std::cout << "DateUtils::isLeapYear(2020) = " << (DateUtils::isLeapYear(2020) ? "true" : "false") << std::endl;
	::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}    