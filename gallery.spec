%define	_rc	RC1
Summary:	Web based photo album viewer and creator.
Summary(pl):	Przegl±darka i generator albumów zdjêæ w postaci stron WWW
Name:		gallery
Version:	1.4.2
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications/Publishing
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	08990a33087dd890c577d4a8452cd1cb
Source1:	http://dl.sourceforge.net/%{name}/pl_PL-pack-%{version}-%{_rc}.tar.gz
# Source1-md5:	0993f84479e608c8fdea215ba1594d3f
URL:		http://gallery.sourceforge.net/
BuildArch:	noarch
Requires:	webserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	gallerydir	/home/services/httpd/html/gallery

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

%prep
%setup -q -a1 -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{gallerydir}

rm -f LICENSE.txt *.bat
mv pl_PL locale
cp -R * $RPM_BUILD_ROOT%{gallerydir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%dir %{gallerydir}
%attr(755,root,root) %{gallerydir}/*.sh
%{gallerydir}/*.php
%{gallerydir}/*.inc
%{gallerydir}/classes
%{gallerydir}/css
%{gallerydir}/docs
%{gallerydir}/errors
%{gallerydir}/html*
%{gallerydir}/images
%{gallerydir}/java
%{gallerydir}/js
%{gallerydir}/layout
%{gallerydir}/platform
%{gallerydir}/po
%{gallerydir}/setup
%{gallerydir}/skins
%{gallerydir}/tools

%dir %{gallerydir}/locale
%{gallerydir}/locale/en_US
%lang(pl) %{gallerydir}/locale/pl_PL
