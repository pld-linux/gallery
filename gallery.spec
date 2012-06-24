Summary:	SVGALib JPEG/GIF/PNG/... picture viewer.
Summary(pl):	Bazowana na SVGALibie przegl�darka do obrazk�w
Name:		gallery
Version:	3.1
Release:	2
License:	GPL
Source0:	ftp://ftp.pld.org.pl/people/malekith/%{name}-%{version}.tar.gz
Group:		Applications/Graphics
Vendor:		Micha� Moskal <malekith@pld.org.pl>
URL:		http://malekith.topnet.pl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	svgalib-devel
BuildRequires:	aalib-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Picture viewer for several gfx formats (PNG, GIF, JPEG, TIFF, PCX,
XPM, BMP, P?M, IFF-{IL,P}BM and othres). No X supported nor needed.
Feauters include scaling, quantizing, sliedeshows and a *lot* of
useless options. Even mouse is supported, it can be used for scaling
and scrolling. Gallery can also display images in text-mode, using
aalib.

%description -l pl
Przegl�darka do obrazk�w w sporej liczbie format�w formatach (PNG,
GIF, JPEG, TIFF, PCX, XPM, BMP, P?M, IFF-{IL,P}BM i inne). �adnych
X�w. Obrazki mo�na skalowa�, kwantyzowa�, robi� slideshowy i wiele
innych bezsensownych rzeczy. Gallery obs�uguje mysz. Mo�e r�wnie�
wy�wietla� obrazki w trybie textowym u�ywaj�c aaliba.

%prep
%setup -q

%build
aclocal
autoconf
%configure \
	--without-debug \
	--without-gziped-man \
	--with-polish-man \
	--with-aalib
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/{man1,pl/man1}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/gallery

install doc/gallery.man		$RPM_BUILD_ROOT%{_mandir}/man1/gallery.1
install doc/gallery-pl.man	$RPM_BUILD_ROOT%{_mandir}/pl/man1/gallery.1
install -m 755 src/gallery	$RPM_BUILD_ROOT%{_bindir}
install lib/*			$RPM_BUILD_ROOT%{_libdir}/gallery
%{__make}			prefix=$RPM_BUILD_ROOT%{_prefix} -C po install

rm -f $RPM_BUILD_ROOT%{_libdir}/gallery/Makefile*

gzip -9nf doc/{AUTHORS,BETA-TESTERS,BUGS,CREDITS,INSTALL,NEWS} \
	  doc/{README,README.pl,TODO}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc doc/{AUTHORS,BETA-TESTERS,BUGS,CREDITS,INSTALL,NEWS,README,TODO}.gz
%doc %lang(pl) doc/README.pl.gz

%attr(755, root, root) %{_bindir}/*
%{_mandir}/man1/*
%dir %{_libdir}/gallery
%{_libdir}/gallery/message.jpg
%attr(755, root, root) %{_libdir}/gallery/config-lynx
%attr(755, root, root) %{_libdir}/gallery/gallery-bugreport
%attr(755, root, root) %{_libdir}/gallery/lsd
