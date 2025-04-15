// include/vector_utils.hxx
#ifndef VECTOR_UTILS_HXX
#define VECTOR_UTILS_HXX

#include <vector>

class VectorUtils {
public:
    static int sum(const std::vector<int>& vec);
    static double average(const std::vector<int>& vec);
    static bool contains(const std::vector<int>& vec, int value);
};

#endif // VECTOR_UTILS_HXX    