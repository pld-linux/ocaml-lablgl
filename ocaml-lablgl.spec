Summary:	OpenGL binding for OCaml
Summary(pl):	Wi±zania OpenGL dla OCamla
Name:		ocaml-lablgl
Version:	0.99
Release:	1
License:	BSD
Group:		Libraries
URL:		http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
Source0:	http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/dist/lablgl-%{version}.tar.gz
# Source0-md5:	5b5ea7889536246c58a5e747d61d6d14
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-labltk-devel
BuildRequires:	OpenGL-devel
BuildRequires:	XFree86-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains files needed to run bytecode executables using
this library.

%description -l pl
LablGL umo¿liwia u¿ywanie OpenGL w OCamlu. Dostêpne s± wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package devel
Summary:	OpenGL binding for OCaml - development part
Summary(pl):	Wi±zania OpenGL dla OCamla - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl
LablGL umo¿liwia u¿ywanie OpenGL w OCamlu. Dostêpne s± wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%package togl
Summary:	Tk widget for lablGL
Summary(pl):	Widget Tk dla lablGL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml-runtime
%requires_eq	ocaml-labltk

%description togl
Togl Tk widget for lablGL, to be used with labltk.

This package contains files needed to run bytecode executables using
this library.

%description togl -l pl
Widget Togl u¿ywaj±cy Tk dla lablGL. Mo¿e byæ on u¿ywany wraz z
labltk.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
u¿ywaj±cych tej biblioteki.

%package togl-devel
Summary:	Tk widget for lablGL - development part
Summary(pl):	Widget Tk dla lablGL - cze¶æ programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
%requires_eq	ocaml-labltk-devel

%description togl-devel
Togl TK widget for lablGL, to be used with labltk.

This package contains files needed to develop OCaml programs using
this library.

%description togl-devel -l pl
Widget Togl u¿ywaj±cy TK dla lablGL. Mo¿e byæ on u¿ywany wraz z
labltk.

Pakiet ten zawiera pliki niezbêdne do tworzenia programów u¿ywaj±cych
tej biblioteki.

%package toplevel
Summary:	OpenGL binding for OCaml - interactive system
Summary(pl):	Wi±zania OpenGL dla OCamla - system interaktywny
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description toplevel
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains OCaml toplevel interactive system linked with
lablgl.

%description toplevel -l pl
LablGL umo¿liwia u¿ywanie OpenGL w OCamlu. Dostêpne s± wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera system interaktywny OCamla zlinkowany z lablgl.

%prep
%setup -q -n lablGL-%{version}

%build
sed -e 's|^TKINCLUDES|#&|;
	s|^GLLIBS.*|GLLIBS = -L%{_prefix}/X11R6/lib -lGL -lGLU -lXmu|;
	s|^COPTS.*|COPTS = %{rpmcflags} -c -fPIC|;' \
	Makefile.config.ex > Makefile.config
%{__make} all opt

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

%{__make} install \
	INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/lablgl \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	BINDIR=$RPM_BUILD_ROOT%{_bindir}

gzip -9nf $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgl/*.mli
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/lablgl/*.mli.gz .

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/{lablgl,togl}
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/lablgl/META <<EOF
# Specifications for the "lablgl" library:
requires = ""
version = "%{version}"
directory = "+lablgl"
archive(byte) = "lablgl.cma"
archive(native) = "lablgl.cmxa"
linkopts = ""
EOF

cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/togl/META <<EOF
# Specifications for the "lablgl" library:
requires = "labgl"
version = "%{version}"
directory = "+lablgl"
archive(byte) = "togl.cma"
archive(native) = "togl.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlllablgl.so

%files togl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlltogl.so

%files togl-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/lablgl/togl.*
%{_libdir}/ocaml/lablgl/libtogl.*
%{_libdir}/ocaml/site-lib/togl

%files devel
%defattr(644,root,root,755)
%doc COPYRIGHT CHANGES README
%dir %{_libdir}/ocaml/lablgl
%{_libdir}/ocaml/lablgl/gl*
%{_libdir}/ocaml/lablgl/lablgl.*
%{_libdir}/ocaml/lablgl/liblablgl.a
%{_libdir}/ocaml/lablgl/raw.*
%{_examplesdir}/%{name}-%{version}
%{_libdir}/ocaml/site-lib/lablgl

%files toplevel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/ocaml/lablgl/lablgltop
