%define		_modname		mmcache
%define		_pkgname	turck-mmcache
%define		_sysconfdir	/etc/php
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)

Summary:	Turck MMCache extension module for PHP
Summary(pl):	Modu� Turck MMCache dla PHP
Name:		php-%{_modname}
Version:	2.4.6
Release:	7
Epoch:		0
License:	GPL
Group:		Libraries
Vendor:		Turck Software
Source0:	http://dl.sourceforge.net/%{_pkgname}/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	bcf671bec2e8b009e9b2d8f8d2574041
URL:		http://turck-mmcache.sourceforge.net
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.238
%{?requires_php_extension}
%{?requires_zend_extension}
Requires:	%{_sysconfdir}/conf.d
Requires:	webserver = apache
Requires:	php-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Turck MMCache is a PHP Accelerator & Encoder. It increases performance
of PHP scripts by caching them in compiled state, so that the overhead
of compiling is almost completely eliminated. Also it uses some
optimizations for speed up of scripts execution.

More information can be find at %{url}.

%description -l pl
Turck MMCache jest akceleratorem i koderem PHP. Zwi�ksza on
efektywno�� skrypt�w PHP poprzez buforowanie ich w postaci
skompilowanej, dzi�ki czemu powt�rne kompilowanie jest praktycznie
wyeliminowane. Wykorzystywane jest tak�e par� optymalizacji, aby
przyspieszy� wykonywanie skrypt�w.

Wi�cej informacji mo�na znale�� pod %{url}.

%package TurckLoader
Summary:	Standalone loader of Turck MMCache's cached files
Summary(pl):	Osobny loader plik�w Turck MMCache
Group:		Libraries
Requires:	webserver = apache
%{?requires_php_extension}
%{?requires_zend_extension}
Provides:	TurckLoader = %{epoch}:%{version}-%{release}

%description TurckLoader
TurckLoader is a standalone loader. You can use files encoded by
without it.

%description TurckLoader -l pl
TurckLoader jest osobnym loaderem. Mo�na u�ywa� plik�w zakodowanych
poprzez Truck MMCache bez niego samego.

%package webinterface
Summary:	WEB interface for Turck MMCache
Summary(pl):	Interfejs WEB dla Turck MMCache
Group:		Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description webinterface
Turck MMCache can be managed through web interface script mmcache.php.
So you need to put this file on your web site. For security reasons it
is recommended to restrict the usage of this script by your local IP.

More information you can find at %{url}.

%description webinterface -l pl
Turck MMCache mo�e by� sterowany ze strony internetowej z
wykorzystaniem skryptu mmcache.php. Jedyne co trzeba zrobi�, to
umie�ci� plik we w�a�ciwym miejscu na stronie internetowej. Z powod�w
bezpiecze�stwa zalecane jest, aby ograniczy� korzystanie ze skryptu do
lokalnego adresu.

Wi�cej informacji mo�na znale�� %{url}.

%prep
%setup -q -n %{_pkgname}-%{version}

%build
phpize
%configure \
	--enable-mmcache=shared \
	--with-php-config=%{_bindir}/php-config
%{__make}

cd TurckLoader
./create_links
phpize
%configure \
	--with-php-config=%{_bindir}/php-config
%{__make}
cd ..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir},%{_bindir}}

install ./modules/mmcache.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}
install ./mmcache_password.php $RPM_BUILD_ROOT%{_bindir}
install ./mmcache.php $RPM_BUILD_ROOT%{_bindir}
install ./TurckLoader/modules/TurckLoader.so $RPM_BUILD_ROOT%{extensionsdir}

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/TurckLoader.ini
; Enable TurckLoader
extension=TurckLoader.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%post TurckLoader
[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart

%postun TurckLoader
if [ "$1" = 0 ]; then
	[ ! -f /etc/apache/conf.d/??_mod_php.conf ] || %service -q apache restart
	[ ! -f /etc/httpd/httpd.conf/??_mod_php.conf ] || %service -q httpd restart
fi

%triggerpostun -- %{name} <= 2.4.6-5
%{_sbindir}/php-module-install remove mmcache %{_sysconfdir}/php.ini

%triggerpostun TurckLoader -- %{name}-TurckLoader <= 2.4.6-5
%{_sbindir}/php-module-install remove TurckLoader %{_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README TODO
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/mmcache.so
%attr(755,root,root) %{_bindir}/encoder.php

%files TurckLoader
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README.loader
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/TurckLoader.ini
%attr(755,root,root) %{extensionsdir}/TurckLoader.so

%files webinterface
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mmcache.php
%attr(755,root,root) %{_bindir}/mmcache_password.php
