#ifndef STRING_FUNCTIONS_HXX
#define STRING_FUNCTIONS_HXX

#include <string>

// 字符串拼接函数
std::string concatenate(const std::string& a, const std::string& b);

// 字符串长度函数
size_t stringLength(const std::string& str);

// 字符串反转函数
std::string reverseString(const std::string& str);

// 检查字符串是否为空
bool isStringEmpty(const std::string& str);

#endif // STRING_FUNCTIONS_HXX    