%global with_python3 0

%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%if %{with_python3}
%{!?python3_sitearch: %define python3_sitearch %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%endif

Name:           python-lxml
Version:        2.2.3
Release:        3
Summary:        ElementTree-like Python bindings for libxml2 and libxslt

Group:          Development/Libraries
License:        BSD
URL:            http://codespeak.net/lxml/
Source0:        http://cheeseshop.python.org/packages/source/l/lxml/lxml-%{version}.tar.gz
#Source0:        http://codespeak.net/lxml/lxml-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libxslt-devel

BuildRequires:  python-devel
BuildRequires:  python-setuptools-devel

%if %{with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%global py3dir  ../python3-lxml-%{version}
%endif

%description
lxml provides a Python binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.

%if %{with_python3}
%package -n python3-lxml
Summary:        ElementTree-like Python 3 bindings for libxml2 and libxslt
Group:          Development/Libraries

%description -n python3-lxml
lxml provides a Python 3 binding to the libxslt and libxml2 libraries.
It follows the ElementTree API as much as possible in order to provide
a more Pythonic interface to libxml2 and libxslt than the default
bindings.  In particular, lxml deals with Python 3 Unicode strings
rather than encoded UTF-8 and handles memory management automatically,
unlike the default bindings.
%endif

%prep
%setup -q -n lxml-%{version}

chmod a-x doc/rest2html.py

%if %{with_python3}
cp -r . %{py3dir}
chmod a-x %{py3dir}/doc/rest2html.py
%endif

%build
CFLAGS="%{optflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build

%if %{with_python3}
pushd %{py3dir}
CFLAGS="%{optflags}" %{__python3} setup.py build
popd
%endif

%install
rm -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install --skip-build --root %{buildroot} --prefix=%{_prefix}

%if %{with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt doc/
%{python_sitearch}/*

%if %{with_python3}
%files -n python3-lxml
%defattr(-,root,root,-)
%doc README.txt LICENSES.txt PKG-INFO CREDITS.txt CHANGES.txt doc/
%{python3_sitearch}/*
%endif
