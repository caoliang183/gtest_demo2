cmake_minimum_required(VERSION 3.10)

project(GTestDemo)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)

# 拉取 Google Test 仓库
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG release-1.11.0
)

# 在构建 Google Test 之前设置运行时库
if (MSVC)
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
endif()

FetchContent_MakeAvailable(googletest)

# 添加测试可执行文件
add_executable(tests
	main.cpp
    test/math_utils_test.cpp
    test/string_utils_test.cpp
    test/vector_utils_test.cpp
    test/date_utils_test.cpp
    src/math_utils.cpp
    src/string_utils.cpp
    src/vector_utils.cpp
    src/date_utils.cpp
)

# 链接 Google Test 库
target_link_libraries(tests gtest gtest_main)

# 包含头文件目录
include_directories(include)

# 添加测试
enable_testing()
add_test(NAME all_tests COMMAND tests)    