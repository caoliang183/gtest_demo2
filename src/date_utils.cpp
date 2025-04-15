// src/date_utils.cpp
#include <ctime>
#include "date_utils.hxx"


bool DateUtils::isLeapYear(int year){
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int DateUtils::daysInMonth(int year, int month){
    static const int days[] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
    if (month == 2 && isLeapYear(year)) {
        return 29;
    }
    return days[month - 1];
}    