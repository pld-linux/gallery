Name:		gallery
Version:	3.0
Release:	1
License:	GPL
Source0:	http://malekith.cnc.pl/bin/%{name}-%{version}.tar.gz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Summary:	SVGALib JPEG/GIF/PNG/... picture viewer.
Summary(pl):	Bazowana na SVGALibie przegl�darka do obrazk�w
Group:		Applications/Graphics
Group(de):	Applikationen/Grafik
Group(pl):	Aplikacje/Grafika
URL:		http://malekith.topnet.pl/
BuildRequires:	svgalib-devel
BuildRequires:	aalib-devel
Vendor:		Micha� Moskal <malekith@pld.org.pl>

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
%configure --without-debug --with-gziped-man --with-polish-man --with-aalib
%{__make}

%install

rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_mandir}/man1 $RPM_BUILD_ROOT%{_mandir}/pl/man1
install doc/gallery.man.gz $RPM_BUILD_ROOT%{_mandir}/man1/gallery.1.gz
install doc/gallery-pl.man.gz $RPM_BUILD_ROOT%{_mandir}/pl/man1/gallery.1.gz
gzip -9nf doc/{AUTHORS,BETA-TESTERS,BUGS,CREDITS,INSTALL,NEWS} \
	doc/{README,README.pl,TODO}
install -d $RPM_BUILD_ROOT%{_bindir}
install -m 755 src/gallery $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_libdir}/gallery
install lib/* $RPM_BUILD_ROOT%{_libdir}/gallery
rm -f $RPM_BUILD_ROOT%{_libdir}/gallery/Makefile*
%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} -C po install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755, root, root) %{_bindir}/*
%{_mandir}/man1/*
%dir %{_libdir}/gallery
%{_libdir}/gallery/message.jpg
%attr(755, root, root) %{_libdir}/gallery/config-lynx
%attr(755, root, root) %{_libdir}/gallery/gallery-bugreport
%attr(755, root, root) %{_libdir}/gallery/lsd

%lang(pl) %{_datadir}/locale/pl/LC_MESSAGES/gallery.mo
%lang(pl) %{_mandir}/pl/man1/*

%doc doc/{AUTHORS,BETA-TESTERS,BUGS,CREDITS,INSTALL,NEWS,README,TODO}.gz
%doc %lang(pl) doc/README.pl.gz
