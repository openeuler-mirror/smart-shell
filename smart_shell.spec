%global python3_pkgversion 3

Name:           python-smart_shell
Version:        1.0.0
Release:        1%{?dist}
Summary:        SmartShell command execution tool

License:        MulanPSL2.0
URL:            https://gitee.com/Delthin/smart_shell
Source:         smart_shell-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires: python3
Requires: python3-pip

%description
SmartShell is a command execution tool that integrates langchain and ReAct to provide an intelligent and convenient shell command execution experience.

%package -n python%{python3_pkgversion}-smsh
Summary:        %{summary}

%description -n python%{python3_pkgversion}-smsh
SmartShell是一个智能命令执行工具，集成了LangChain和ReAct，提供智能且便捷的shell命令执行体验。

%prep
%autosetup -p1 -n smart_shell-%{version}

%build
%py3_build

%install
%py3_install

%files -n python%{python3_pkgversion}-smsh
%doc README.md
%license LICENSE
%{_bindir}/*
%{python3_sitelib}/smsh/
%{python3_sitelib}/smart_shell-*.egg-info/
%exclude %{python3_sitelib}/tests/*

%changelog
* Thu Aug 29 2024 Delthin <1059661071@qq.com> - 1.0.0-1
- First release