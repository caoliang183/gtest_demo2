#include <algorithm>
#include "..\include/string_functions.hxx"


// 字符串拼接函数的实现
std::string concatenate(const std::string& a, const std::string& b){
	
    return a + b;
}

// 字符串长度函数的实现
size_t stringLength(const std::string& str){
	
    return str.length();
}

// 字符串反转函数的实现
std::string reverseString(const std::string& str){
	
    std::string result = str;
    std::reverse(result.begin(), result.end());
    return result;
}

// 检查字符串是否为空的实现
bool isStringEmpty(const std::string& str){
	
    return str.empty();
}