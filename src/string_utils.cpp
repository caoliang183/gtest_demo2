// src/string_utils.cpp
#include <algorithm>
#include <cctype>
#include <string>
#include "string_utils.hxx"

std::string StringUtils::toUpperCase(const std::string& str){
	
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), [](unsigned char c){
		
        return std::toupper(c);
    });
    return result;
}

std::string StringUtils::toLowerCase(const std::string& str){
	
    std::string result = str;
    std::transform(result.begin(), result.end(), result.begin(), [](unsigned char c){
		
        return std::tolower(c);
    });
    return result;
}

bool StringUtils::startsWith(const std::string& str, const std::string& prefix){
	
    return str.rfind(prefix, 0) == 0;
}

bool StringUtils::endsWith(const std::string& str, const std::string& suffix){
	
    if (str.length() < suffix.length()){
		
        return false;
    }
    return str.compare(str.length() - suffix.length(), suffix.length(), suffix) == 0;
	
}    