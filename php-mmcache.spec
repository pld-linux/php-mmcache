
%define		php_prefix	/usr
%define		_name		mmcache
%define		_pkgname	turck-mmcache

Summary:	Turck MMCache extension module for PHP
Summary(pl):	Modu³ Turck MMCache dla PHP
Name:		php-%{_name}
Version:	2.3.19
Release:	0.1
Epoch:		0
License:	GPL
Group:		Libraries
Vendor:		Turck Software
Source0:	http://dl.sourceforge.net/sourceforge/%{_pkgname}/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	6adfff394a13aa181eb127caeed7224b
URL:		http://www.turcksoft.com/en/e_mmc.htm
BuildRequires:	php-devel >= 4.1
BuildRequires:	automake
Requires:	apache >= 1.3
#Requires:	mod_php >= 4.1
Provides:	mmcache
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Turck MMCache is a PHP Accelerator & Encoder. It increases performance
of PHP scripts by caching them in compiled state, so that the overhead
of compiling is almost completely eliminated. Also it uses some
optimizations for speed up of scripts execution.

%description -l pl
Turck MMCache jest akceleratorem i koderem PHP. Zwiêksza on efektywno¶æ
skryptów PHP poprzez cachowanie ich w postaci skompilowanej, zatem
powtórne kompilowanie jest praktycznie wyeliminowane. Wykorzystywane
jest tak¿e pare optymalizacji, aby przyspieszyæ wykonywanie skryptów.

%prep
%setup -q -n %{_pkgname}-%{version}
%{php_prefix}/bin/phpize

%build
%{__aclocal}
%configure --enable-mmcache=shared --with-php-config=%{php_prefix}/bin/php-config
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT
install -D ./modules/mmcache.so $RPM_BUILD_ROOT%{extensionsdir}/mmcache.so

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
%{_sbindir}/php-module-install install mmcache %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mmcache %{_sysconfdir}/php.ini
fi

%postun

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README README.loader TODO
%attr(755,root,root) %{extensionsdir}/mmcache.so
