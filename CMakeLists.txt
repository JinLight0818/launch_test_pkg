cmake_minimum_required(VERSION 3.20)
project(launch_test_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(launch_testing_ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# === Talker нод ===

add_executable(talker src/talker.cpp)
target_link_libraries(talker PUBLIC rclcpp::rclcpp ${std_msgs_TARGETS})
install(TARGETS talker DESTINATION lib/${PROJECT_NAME})

# === Launch файлууд ===

install(
  DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# === Launch тест ===

add_launch_test(test/test_talker_launch.py)

ament_package()

