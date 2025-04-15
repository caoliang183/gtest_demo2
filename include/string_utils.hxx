// include/string_utils.hxx
#ifndef STRING_UTILS_HXX
#define STRING_UTILS_HXX

#include <string>

class StringUtils {
public:
    static std::string toUpperCase(const std::string& str);
    static std::string toLowerCase(const std::string& str);
    static bool startsWith(const std::string& str, const std::string& prefix);
    static bool endsWith(const std::string& str, const std::string& suffix);
};

#endif // STRING_UTILS_HXX    