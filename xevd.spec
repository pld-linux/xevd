#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	eXtra-fast Essential Video Decoder (MPEG-5 EVC)
Summary(pl.UTF-8):	eXtra-fast Essential Video Decoder - szybki dekoder obrazu MPEG-5 EVC
Name:		xevd
Version:	0.4.1
%define	gitref	%{version}-4e76654c
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/mpeg5/xevd/releases
Source0:	https://github.com/mpeg5/xevd/archive/v%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	d1642df4b69196430e669d6b278e73d7
Patch0:		%{name}-string.patch
Patch1:		%{name}-link.patch
URL:		https://github.com/mpeg5/xevd
BuildRequires:	cmake >= 3.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The eXtra-fast Essential Video Decoder (XEVD) is an opensource and
fast MPEG-5 EVC decoder.

MPEG-5 Essential Video Coding (EVC) is a video compression standard of
ISO/IEC Moving Picture Experts Group (MPEG). The main goal of the EVC
is to provide a significantly improved compression capability over
existing video coding standards with timely publication of terms.

This package contains the library with Main Profile (with additional
tools).

%description -l pl.UTF-8
XEVD (eXtra-fast Essential Video Decoder - bardzo szybki dekoder
obrazu zasadniczego) to szybki, mający otwarte źródła dekoder MPEG-5
EVC.

MPEG-5 Essential Video Coding (EVC) to standard kompresji obrazu
tworzony przez ISO/IEC Moving Picture Experts Group (MPEG). Głównym
celem EVC jest zapewnienie znacząco lepszych mozliwości kompresji niż
istniejące standardy kodowania obrazu.

Ten pakiet zawiera bibliotekę o profilu Main (z dodatkowymi
narzędziami).

%package devel
Summary:	Header files for XEVD library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki XEVD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for XEVD library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki XEVD.

%package static
Summary:	Static XEVD library
Summary(pl.UTF-8):	Statyczna biblioteka XEVD
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static XEVD library.

%description static -l pl.UTF-8
Statyczna biblioteka XEVD.

%package base
Summary:	eXtra-fast Essential Video Decoder (MPEG-5 EVC) - Baseline Profile
Summary(pl.UTF-8):	eXtra-fast Essential Video Decoder - szybki dekoder obrazu MPEG-5 EVC - profil Baseline
Group:		Libraries

%description base
The eXtra-fast Essential Video Decoder (XEVD) is an opensource and
fast MPEG-5 EVC decoder.

MPEG-5 Essential Video Coding (EVC) is a video compression standard of
ISO/IEC Moving Picture Experts Group (MPEG). The main goal of the EVC
is to provide a significantly improved compression capability over
existing video coding standards with timely publication of terms.

This package contains the library with Baseline Profile (which contain
only technologies that are older than 20 years or otherwise freely
available for use in the standard).

%description base -l pl.UTF-8
XEVD (eXtra-fast Essential Video Decoder - bardzo szybki dekoder
obrazu zasadniczego) to szybki, mający otwarte źródła dekoder MPEG-5
EVC.

MPEG-5 Essential Video Coding (EVC) to standard kompresji obrazu
tworzony przez ISO/IEC Moving Picture Experts Group (MPEG). Głównym
celem EVC jest zapewnienie znacząco lepszych mozliwości kompresji niż
istniejące standardy kodowania obrazu.

Ten pakiet zawiera bibliotekę o profilu Baseline (zawierający jedynie
technologie starsze niż 20 lat albo w inny sposób wolnodostępne do
użycia w standardzie).

%package base-devel
Summary:	Header files for XEVD library (Baseline Profile)
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki XEVD (profil Baseline)
Group:		Development/Libraries
Requires:	%{name}-base = %{version}-%{release}

%description base-devel
Header files for XEVD library (Baseline Profile).

%description base-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki XEVD (profil Baseline).

%package base-static
Summary:	Static XEVD library (Baseline Profile)
Summary(pl.UTF-8):	Statyczna biblioteka XEVD (profil Baseline)
Group:		Development/Libraries
Requires:	%{name}-base-devel = %{version}-%{release}

%description base-static
Static XEVD library (Baseline Profile).

%description base-static -l pl.UTF-8
Statyczna biblioteka XEVD (profil Baseline).

%prep
%setup -q -n %{name}-%{gitref}
%patch0 -p1
%patch1 -p1

echo "v%{version}" > version.txt

%build
install -d build-main
cd build-main
%cmake .. \
	-DXEVD_APP_STATIC_BUILD=OFF

%{__make}
cd ..

install -d build-base
cd build-base
%cmake .. \
	-DSET_PROF=BASE \
	-DXEVD_APP_STATIC_BUILD=OFF

%{__make}
%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build-main install \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_libdir}/xevd/lib*.a $RPM_BUILD_ROOT%{_libdir}

%{__make} -C build-base install \
	DESTDIR=$RPM_BUILD_ROOT
%{__mv} $RPM_BUILD_ROOT%{_libdir}/xevdb/lib*.a $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	base -p /sbin/ldconfig
%postun	base -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/xevd_app
%attr(755,root,root) %{_libdir}/libxevd.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxevd.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxevd.so
%{_includedir}/xevd
%{_pkgconfigdir}/xevd.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libxevd.a
%endif

%files base
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/xevdb_app
%attr(755,root,root) %{_libdir}/libxevdb.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxevdb.so.0

%files base-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxevdb.so
%{_includedir}/xevdb
%{_pkgconfigdir}/xevdb.pc

%if %{with static_libs}
%files base-static
%defattr(644,root,root,755)
%{_libdir}/libxevdb.a
%endif
