Summary:	Web based photo album viewer and creator
Summary(pl.UTF-8):	Przeglądarka i generator albumów zdjęć w postaci stron WWW
Name:		gallery
Version:	1.5.10
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/gallery/%{name}-%{version}.tar.gz
# Source0-md5:	a8147e62b248baf25cdd2a79a63453eb
Source1:	http://dl.sourceforge.net/gallery/pl_PL-1.5.2.tar.gz
# Source1-md5:	1dd07a63d96299d8f5e4cc03342d318e
Source2:	%{name}-apache.conf
Patch0:		%{name}-PLD.patch
URL:		http://gallery.menalto.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(gettext)
Requires:	webapps
Requires:	webserver(php) >= 4.1.0
#Suggests:	apache(mod_rewrite)
#Suggests:	jhead
#Suggests:	jpegtran
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir	%{_datadir}/%{_webapp}

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
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Gallery
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Gallery installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfigurac Gallery po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q
%patch0 -p1

tar zxf %{SOURCE1} -C locale
rm -f LICENSE.txt *.bat

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/var/lib/gallery/albums}

cp -a *.{php,inc,sh} $RPM_BUILD_ROOT%{_appdir}
cp -a classes contrib css docs help html html_wrap images $RPM_BUILD_ROOT%{_appdir}
cp -a includes java js layout lib locale platform skins tools $RPM_BUILD_ROOT%{_appdir}
# in /var because of setup/resetadmin file
cp -a setup $RPM_BUILD_ROOT/var/lib/gallery
ln -s /var/lib/gallery/setup $RPM_BUILD_ROOT%{_appdir}
ln -s %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.php
rm -f $RPM_BUILD_ROOT%{_appdir}/{AUTHORS,ChangeLog*,README}

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/config.php
touch $RPM_BUILD_ROOT%{_sysconfdir}/htaccess
ln -s %{_sysconfdir}/htaccess $RPM_BUILD_ROOT%{_appdir}/.htaccess

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
%doc AUTHORS ChangeLog* README
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/htaccess
%dir %{_appdir}
%dir /var/lib/gallery
%dir %attr(770,root,http) /var/lib/gallery/albums
%{_appdir}/.htaccess
%{_appdir}/*.php
%{_appdir}/*.inc
%{_appdir}/classes
%{_appdir}/contrib
%{_appdir}/css
%{_appdir}/docs
%{_appdir}/html*
%{_appdir}/help
%{_appdir}/images
%{_appdir}/includes
%{_appdir}/java
%{_appdir}/js
%{_appdir}/layout
%{_appdir}/lib
%{_appdir}/platform
%{_appdir}/skins
%{_appdir}/tools

%dir %{_appdir}/locale
%{_appdir}/locale/en_US
%lang(pl) %{_appdir}/locale/pl_PL

%files setup
%defattr(644,root,root,755)
%attr(755,root,root) %{_appdir}/*.sh
%{_appdir}/setup
%{_appdir}/config.php
/var/lib/gallery/setup
