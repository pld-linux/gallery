# TODO:
# - use external libs, not the included ones: pear, smarty, adodb
# - move to separate packages each: theme, module.
Summary:	Web based photo album viewer and creator
Summary(pl):	Przegl±darka i generator albumów zdjêæ w postaci stron WWW
Name:		gallery
Version:	2.1.1a
%define		_snap	20060728
Release:	1.%{_snap}.0.1
License:	GPL
Group:		Applications/Publishing
#Source0:	http://dl.sourceforge.net/gallery/%{name}-%{version}-full.tar.gz
Source0:	http://galleryupdates.jpmullan.com/G2/%{name}-nightly.tar.gz
# Source0-md5:	6d609d4bbce81c7719799ad953a8b7d1
Source1:	%{name}-apache.conf
URL:		http://gallery.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	php-gettext
Requires:	php-pcre
Requires:	php >= 3:4.1.0
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

%description -l pl
Gallery jest albumem zdjêæ, który posiadaj kreatora konfiguracji i
pozwala u¿ytkownikom tworzyæ i zarz±dzaæ albumami przez intuicyjny
interfejs WWW. Zarz±dzanie zdjêciami umo¿liwia automatyczne tworzenie
miniatur, zmianê wielko¶ci obrazów, obrót, zmianê kolejno¶ci
wy¶wietlania, itp. Albumy mog± posiadaæ indywidualne uprawnienia.

%package setup
Summary:	Gallery setup package
Summary(pl):	Pakiet do wstêpnej konfiguracji Gallery
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}
Conflicts:	external-gallery-module

%description setup
Install this package to configure initial Gallery installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl
Ten pakiet nale¿y zainstalowaæ w celu wstêpnej konfiguracji Gallery po
pierwszej instalacji. Potem nale¿y go odinstalowaæ, jako ¿e
pozostawienie plików instalacyjnych mog³oby byæ niebezpieczne.

%prep
%setup -q -n %{name}2

rm -f LICENSE.txt *.bat

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir},/var/lib/gallery/albums}

cp -a *.{php,inc} $RPM_BUILD_ROOT%{_appdir}
cp -a images lib modules themes $RPM_BUILD_ROOT%{_appdir}
cp -a install upgrade $RPM_BUILD_ROOT%{_appdir}
# in /var because of setup/resetadmin file
#cp -a setup $RPM_BUILD_ROOT/var/lib/gallery
#ln -s /var/lib/gallery/setup $RPM_BUILD_ROOT%{_appdir}

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

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/login.txt
%dir %{_appdir}
%dir /var/lib/gallery
%dir %attr(770,root,http) /var/lib/gallery/albums
%{_appdir}/*.php
%{_appdir}/*.inc
%{_appdir}/login.txt
%{_appdir}/images
%{_appdir}/lib
%{_appdir}/modules
%{_appdir}/themes
%{_appdir}/upgrade

%files setup
%defattr(644,root,root,755)
%{_appdir}/config.php
%{_appdir}/install
#/var/lib/gallery/setup
