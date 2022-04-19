%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-rmf-fleet-adapter
Version:        1.4.0
Release:        3%{?dist}%{?release_suffix}
Summary:        ROS rmf_fleet_adapter package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-humble-rclcpp
Requires:       ros-humble-rclcpp-components
Requires:       ros-humble-rmf-battery
Requires:       ros-humble-rmf-dispenser-msgs
Requires:       ros-humble-rmf-door-msgs
Requires:       ros-humble-rmf-fleet-msgs
Requires:       ros-humble-rmf-ingestor-msgs
Requires:       ros-humble-rmf-lift-msgs
Requires:       ros-humble-rmf-task
Requires:       ros-humble-rmf-task-msgs
Requires:       ros-humble-rmf-traffic
Requires:       ros-humble-rmf-traffic-ros2
Requires:       ros-humble-rmf-utils
Requires:       ros-humble-std-msgs
Requires:       ros-humble-ros-workspace
BuildRequires:  eigen3-devel
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-rclcpp-components
BuildRequires:  ros-humble-rmf-battery
BuildRequires:  ros-humble-rmf-dispenser-msgs
BuildRequires:  ros-humble-rmf-door-msgs
BuildRequires:  ros-humble-rmf-fleet-msgs
BuildRequires:  ros-humble-rmf-ingestor-msgs
BuildRequires:  ros-humble-rmf-lift-msgs
BuildRequires:  ros-humble-rmf-task
BuildRequires:  ros-humble-rmf-task-msgs
BuildRequires:  ros-humble-rmf-traffic
BuildRequires:  ros-humble-rmf-traffic-ros2
BuildRequires:  ros-humble-rmf-utils
BuildRequires:  ros-humble-std-msgs
BuildRequires:  yaml-cpp-devel
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-humble-ament-cmake-catch2
BuildRequires:  ros-humble-rmf-cmake-uncrustify
%endif

%description
Fleet Adapter package for RMF fleets.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Tue Apr 19 2022 Grey <grey@openrobotics.org> - 1.4.0-3
- Autogenerated by Bloom

* Tue Feb 08 2022 Grey <grey@openrobotics.org> - 1.4.0-2
- Autogenerated by Bloom

