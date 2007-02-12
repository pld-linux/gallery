# TODO:
# - use external libs, not the included ones: pear, smarty, adodb
# - move to separate packages each: theme, module.
%define	_snap	20060728
%define	_rel	0.8
Summary:	Web based photo album viewer and creator
Summary(pl.UTF-8):   Przeglądarka i generator albumów zdjęć w postaci stron WWW
Name:		gallery
Version:	2.1.1a
Release:	1.%{_snap}.%{_rel}
License:	GPL
Group:		Applications/Publishing
#Source0:	http://dl.sourceforge.net/gallery/%{name}-%{version}-full.tar.gz
Source0:	http://galleryupdates.jpmullan.com/G2/%{name}-nightly.tar.gz
# Source0-md5:	6d609d4bbce81c7719799ad953a8b7d1
Source1:	%{name}-apache.conf
Patch0:		%{name}-setup.patch
URL:		http://gallery.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(gettext)
Requires:	php(pcre)
Requires:	webapps
Requires:	webserver(php) >= 4.1.0
#Suggests:	apache(mod_rewrite)
#Suggests:	jhead
#Suggests:	jpegtran
#Suggests:	php-gd
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Gallery is a photo album that includes a config wizard and lets users
create and maintain albums via an intuitive Web interface. Photo
management includes automatic thumbnail creation, image resizing,
rotation, ordering and more. Albums can have read, write, and caption
permissions per individual.

%description -l pl.UTF-8
Gallery jest albumem zdjęć, który posiadaj kreatora konfiguracji i
pozwala użytkownikom tworzyć i zarządzać albumami przez intuicyjny
interfejs WWW. Zarządzanie zdjęciami umożliwia automatyczne tworzenie
miniatur, zmianę wielkości obrazów, obrót, zmianę kolejności
wyświetlania, itp. Albumy mogą posiadać indywidualne uprawnienia.

%package setup
Summary:	Gallery setup package
Summary(pl.UTF-8):   Pakiet do wstępnej konfiguracji Gallery
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Conflicts:	external-gallery-module

%description setup
Install this package to configure initial Gallery installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Gallery po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -n %{name}2
%patch0 -p1

rm -f LICENSE.txt *.bat

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/var/lib/gallery/albums}

cp -a *.{php,inc} $RPM_BUILD_ROOT%{_appdir}
cp README.html $RPM_BUILD_ROOT%{_appdir}
cp -a images lib modules themes $RPM_BUILD_ROOT%{_appdir}
cp -a install upgrade $RPM_BUILD_ROOT%{_appdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/config.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/login.txt
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.php
ln -s %{_sysconfdir}/login.txt $RPM_BUILD_ROOT%{_appdir}/login.txt

## Cleanup modules that are avaible in separate packages:
for module in exif; do
	rm -rf $RPM_BUILD_ROOT%{_appdir}/modules/$module
done

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} < 1.5.2-0.13
/usr/sbin/webapp register httpd %{_webapp}
%service -q httpd reload

%files
%defattr(644,root,root,755)
%doc README*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/login.txt
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%dir %{_appdir}
%dir /var/lib/gallery
%dir %attr(770,root,http) /var/lib/gallery/albums
%{_appdir}/login.txt
%{_appdir}/*.php
%{_appdir}/*.inc
%{_appdir}/images
%{_appdir}/lib
%{_appdir}/modules
%{_appdir}/themes

%files setup
%defattr(644,root,root,755)
%{_appdir}/README.html
%{_appdir}/config.php
%{_appdir}/install
%{_appdir}/upgrade
