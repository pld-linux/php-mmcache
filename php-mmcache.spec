%define		_name		mmcache
%define		_pkgname	turck-mmcache

Summary:	Turck MMCache extension module for PHP
Summary(pl):	Modu³ Turck MMCache dla PHP
Name:		php-%{_name}
Version:	2.3.19
Release:	0.3
License:	GPL
Group:		Libraries
Vendor:		Turck Software
Source0:	http://dl.sourceforge.net/sourceforge/%{_pkgname}/%{_pkgname}-%{version}.tar.gz
# Source0-md5:	6adfff394a13aa181eb127caeed7224b
URL:		http://www.turcksoft.com/en/e_mmc.htm
BuildRequires:	php-devel >= 4.1
BuildRequires:	automake
Requires:	php-zlib
Requires:	apache >= 1.3
Requires(post,preun):	php-common >= 4.1
Requires:	php >= 4.1
Requires:	php-common >= 4.1
Provides:	php-mmcache = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
Turck MMCache is a PHP Accelerator & Encoder. It increases performance
of PHP scripts by caching them in compiled state, so that the overhead
of compiling is almost completely eliminated. Also it uses some
optimizations for speed up of scripts execution.

Please don't use Turck MMCache Encoder for commercial purpose until
Turck MMCache version 2.4.0 is out. The format of encoded files may be
changed and it is possible that the old formats will not be supported.

More information can be find at %{url}

%description -l pl
Turck MMCache jest akceleratorem i koderem PHP. Zwiêksza on
efektywno¶æ skryptów PHP poprzez cachowanie ich w postaci
skompilowanej, zatem powtórne kompilowanie jest praktycznie
wyeliminowane. Wykorzystywane jest tak¿e pare optymalizacji, aby
przyspieszyæ wykonywanie skryptów.

Turck MMCache Encoder nie powinien byæ u¿ywany do celów komercyjnych a¿
do wydania wersji 2.4.0. Byæ mo¿e zostanie zmieniony format plików i
stare wersje nie bêd± obs³ugiwane.

Wiêcej informacji znajdziesz na %{url}

%package TurckLoader
Summary:	Standalone loader of Turck MMCache's cached files
Summary(pl):	Osobny loader plikow Turck MMCache.
Group:		Libraries
# FIXME: czy te wszystkie Req te¿?
Requires:	apache >= 1.3
Requires(post,preun):	php-common >= 4.1
# FIXME: powinno byæ php, php-common czy to i to?
Requires:	php >= 4.1
Requires:	php-common >= 4.1
Provides:	TurckLoader = %{epoch}:%{version}-%{release}

%description TurckLoader
TurckLoader is a standalone loader. You can use files encoded by
without it.

%description TurckLoader -l pl
TurckLoader jest osobnym loaderem. Mo¿esz u¿ywaæ plików zakodowanych
poprzez Truck MMCache bez niego samego.

%package webinterface
Summary:	WEB interface for Turck MMCache
Summary(pl):	Interfejs WEB dla Turck MMCache
Group:		Libraries
Requires:	php >= 4.1
Requires:	php-mmcache = %{epoch}:%{version}-%{release}
Provides:	php-mmcache-webinterface = %{epoch}:%{version}-%{release}

%description webinterface
Turck MMCache can be managed through web interface script mmcache.php.
So you need to put this file on your web site. For security reasons it
is recommended to restrict the usage of this script by your local IP.

More information you can find at %{url}

%description webinterface -l pl
Turck MMCache moze byæ sterowany ze strony internetowej korzystaj±c ze
skryptu mmcache.php. Jedyne co musisz zrobiæ, to umie¶ciæ plik we
w³a¶ciwym miejscu na stronie internetowej. Z powodów bezpieczeñstwa
zalecane jest, aby ograniczyæ korzystanie ze skryptu do lokalnego
adresu.

Wiêcej informacji znajdzie¿ na %{url}

%prep
%setup -q -n %{_pkgname}-%{version}

%build
phpize
%{__aclocal}
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
install -d $RPM_BUILD_ROOT%{extensionsdir}
install -d $RPM_BUILD_ROOT%{_bindir}

install ./modules/mmcache.so $RPM_BUILD_ROOT%{extensionsdir}
install ./encoder.php $RPM_BUILD_ROOT%{_bindir}

install ./TurckLoader/modules/TurckLoader.so $RPM_BUILD_ROOT%{extensionsdir}


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install mmcache %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove mmcache %{_sysconfdir}/php.ini
fi

%post TurckLoader
%{_sbindir}/php-module-install install TurckLoader %{_sysconfdir}/php.ini

%preun TurckLoader
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove TurckLoader %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL README TODO
%attr(755,root,root) %{extensionsdir}/mmcache.so
%attr(755,root,root) %{_bindir}/encoder.php

%files TurckLoader
%defattr(644,root,root,755)
%doc CREDITS EXPERIMENTAL
%attr(755,root,root) %{extensionsdir}/TurckLoader.so

%files webinterface
%defattr(644,root,root,755)
# FIXME: czy tak rzeczywi¶cie powinno/mo¿e byæ??
%doc mmcache{,_password}.php
