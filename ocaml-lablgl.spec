#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%if %{without ocaml_opt}
%define		_enable_debug_packages	0
%endif

%define		ocaml_ver	1:3.09.2
Summary:	OpenGL binding for OCaml
Summary(pl.UTF-8):	Wiązania OpenGL dla OCamla
Name:		ocaml-lablgl
Version:	1.06
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/garrigue/lablgl/releases
Source0:	https://github.com/garrigue/lablgl/archive/v%{version}/lablgl-%{version}.tar.gz
# Source0-md5:	8ee7a37b016095c4f7cd066f0ebd4436
URL:		http://wwwfun.kurims.kyoto-u.ac.jp/soft/olabl/lablgl.html
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	OpenGL-glut-devel >= 3.7
BuildRequires:	ocaml >= %{ocaml_ver}
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-labltk-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel >= 4.0
BuildRequires:	xorg-lib-libXmu-devel
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains files needed to run bytecode executables using
this library.

%description -l pl.UTF-8
LablGL umożliwia używanie OpenGL w OCamlu. Dostępne są wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	OpenGL binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania OpenGL dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
LablGL umożliwia używanie OpenGL w OCamlu. Dostępne są wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%package togl
Summary:	Tk widget for lablGL
Summary(pl.UTF-8):	Widget Tk dla lablGL
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml-labltk
%requires_eq	ocaml-runtime

%description togl
Togl Tk widget for lablGL, to be used with labltk.

This package contains files needed to run bytecode executables using
this library.

%description togl -l pl.UTF-8
Widget Togl używający Tk dla lablGL. Może być on używany wraz z
labltk.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package togl-devel
Summary:	Tk widget for lablGL - development part
Summary(pl.UTF-8):	Widget Tk dla lablGL - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
%requires_eq	ocaml-labltk-devel

%description togl-devel
Togl Tk widget for lablGL, to be used with labltk.

This package contains files needed to develop OCaml programs using
this library.

%description togl-devel -l pl.UTF-8
Widget Togl używający Tk dla lablGL. Może być on używany wraz z
labltk.

Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%package glut
Summary:	GLUT binding for OCaml
Summary(pl.UTF-8):	Wiązanie OCamla dla biblioteki GLUT
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml-runtime

%description glut
The lablglut library is an OCaml binding for GLUT version 3.7. GLUT
(GL Utility Toolkit) is a portable windowing library for OpenGL,
written by Mark Kilgard.

%description glut -l pl.UTF-8
Biblioteka lablglut to wiązanie OCamla dla biblioteki GLUT w wersji
3.7. GLUT (czyli GL Utility Toolkit) to przenośna biblioteka okienkowa
dla OpenGL-a, napisana przez Marka Kilgarda.

%package glut-devel
Summary:	GLUT binding for OCaml - development part
Summary(pl.UTF-8):	Wiązanie OCamla dla biblioteki GLUT - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description glut-devel
This package contains development files for GLUT binding for OCaml.

%description glut-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne wiązania OCamla dla
biblioteki GLUT.

%package toplevel
Summary:	OpenGL binding for OCaml - interactive system
Summary(pl.UTF-8):	Wiązania OpenGL dla OCamla - system interaktywny
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description toplevel
LablGL is an OpenGL interface for Objective Caml. All of the GL and
GLU libraries are available.

This package contains OCaml toplevel interactive system linked with
lablgl.

%description toplevel -l pl.UTF-8
LablGL umożliwia używanie OpenGL w OCamlu. Dostępne są wszystkie
biblioteki GL i GLU.

Pakiet ten zawiera system interaktywny OCamla skonsolidowany z lablgl.

%prep
%setup -q -n lablgl-%{version}

find LablGlut/examples -name '*.ml' -print0 | xargs --null \
	%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+lablglut(\s|$),#!%{_bindir}/lablglut\1,' \

%build
sed -e 's|^\(X\|TK\)INCLUDES|#&|;
	s|^GLLIBS.*|GLLIBS = -lGL -lGLU -lXmu|;
	s|^COPTS.*|COPTS = %{rpmcflags} -c -fPIC|;' \
	Makefile.config.ex > Makefile.config
%{__make} -j1 all %{?with_ocaml_opt:opt}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml/stublibs} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/{LablGlut,Togl}

%{__make} install \
	INSTALLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL \
	DLLDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	BINDIR=$RPM_BUILD_ROOT%{_bindir}

%{__mv} $RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL/*.mli .

cp -r LablGlut/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/LablGlut
cp -r Togl/examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}/Togl

cp -p META $RPM_BUILD_ROOT%{_libdir}/ocaml/lablGL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYRIGHT CHANGES README
%dir %{_libdir}/ocaml/lablGL
%{_libdir}/ocaml/lablGL/META
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlllablgl.so

%files devel
%defattr(644,root,root,755)
%doc *.mli
%{_libdir}/ocaml/lablGL/build.ml
%{_libdir}/ocaml/lablGL/gl*
%{_libdir}/ocaml/lablGL/lablgl.*
%{_libdir}/ocaml/lablGL/liblablgl.a
%{_libdir}/ocaml/lablGL/raw.*
%{_examplesdir}/%{name}-%{version}

%files glut
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlllablglut.so

%files glut-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/lablGL/lablglut.*
%{_libdir}/ocaml/lablGL/liblablglut.a

%files togl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dlltogl.so

%files togl-devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/lablGL/togl.*
%{_libdir}/ocaml/lablGL/libtogl.a

%files toplevel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lablgl
%attr(755,root,root) %{_bindir}/lablglut
