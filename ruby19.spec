%define major           1
%define minor           9
%define teeny           3
%define rubyver         %{major}.%{minor}.%{teeny}
%define ruby_apiversion %{major}.%{minor}.1
%define rubyminorver    p0

Name:           ruby
Version:        %{rubyver}%{rubyminorver}
Release:        1%{?dist}
License:        Ruby License/GPL - see COPYING
URL:            http://www.ruby-lang.org/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  readline readline-devel ncurses ncurses-devel gdbm gdbm-devel glibc-devel tcl-devel gcc unzip openssl-devel db4-devel byacc make
Source0:        ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{rubyver}-%{rubyminorver}.tar.gz
Summary:        An interpreter of object-oriented scripting language
Group:          Development/Languages
Provides:       rubygems = %{major}.%{minor}
Obsoletes:      rubygems < %{major}.%{minor}

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.

%package libs
Summary:        Libraries necessary to run Ruby
Group:          Development/Libraries
Provides:       ruby(abi) = %{major}.%{minor}

%description libs
This package includes the libraries necessary to run Ruby.

%package irb
Summary:        The Interactive Ruby
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}
Provides:       irb = %{version}-%{release}
Obsoletes:      irb <= %{version}-%{release}

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.

%package rdoc
Summary:        A tool to generate documentation from Ruby source files
Group:          Development/Languages
Requires:       %{name}-irb = %{version}-%{release}
Provides:       rdoc = %{version}-%{release}
Obsoletes:      rdoc <= %{version}-%{release}

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).

%package devel
Summary:        A Ruby development environment
Group:          Development/Languages
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.

%package docs
Summary:        Manuals and FAQs for scripting language Ruby
Group:          Documentation

%description docs
Manuals and FAQs for the object-oriented scripting language Ruby.

%package ri
Summary:        Ruby interactive reference
Group:          Documentation
Requires:       %{name}-rdoc = %{version}-%{release}
Provides:       ri = %{version}-%{release}
Obsoletes:      ri <= %{version}-%{release}

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.

%prep
%setup -n ruby-%{rubyver}-%{rubyminorver}

%build
export CFLAGS="$RPM_OPT_FLAGS -Wall -fno-strict-aliasing"

%configure \
  --enable-shared \
  --disable-rpath \
  --without-X11 \
  --without-tk \
  --includedir=%{_includedir}/ruby \
  --libdir=%{_libdir}

make %{?_smp_mflags}

%install
# start with a clean build root
rm -rf $RPM_BUILD_ROOT

# installing binaries ...
make install DESTDIR=$RPM_BUILD_ROOT

#we don't want to keep the src directory
##rm -rf $RPM_BUILD_ROOT/usr/src

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}/*
%exclude %{_bindir}/irb
%exclude %{_bindir}/ri
%exclude %{_bindir}/rdoc
%{_datadir}/man/man*/*
%exclude %{_datadir}/ri

%files libs
%defattr(-, root, root, -)
%{_libdir}/libruby*
%{_libdir}/%{name}
%exclude %{_libdir}/%{name}/%{ruby_apiversion}/irb.rb
%exclude %{_libdir}/%{name}/%{ruby_apiversion}/irb
%exclude %{_libdir}/%{name}/%{ruby_apiversion}/rdoc
%exclude %{_libdir}/%{name}/%{ruby_apiversion}/rdoc.rb

%files irb
%defattr(-, root, root, -)
%{_bindir}/irb
%{_libdir}/%{name}/%{ruby_apiversion}/irb.rb
%{_libdir}/%{name}/%{ruby_apiversion}/irb

%files rdoc
%defattr(-, root, root, -)
%{_bindir}/rdoc
%{_libdir}/%{name}/%{ruby_apiversion}/rdoc
%{_libdir}/%{name}/%{ruby_apiversion}/rdoc.rb

%files devel
%defattr(-, root, root, -)
%doc README.EXT
%lang(ja) %doc README.EXT.ja
%{_includedir}/ruby
%{_libdir}/pkgconfig/ruby-1.9.pc

%files docs
%defattr(-, root, root, -)
%doc README COPYING ChangeLog GPL LEGAL NEWS ToDo
%lang(ja) %doc README.ja COPYING.ja

%files ri
%defattr(-, root, root, -)
%{_bindir}/ri
%{_datadir}/ri

%changelog
* Thu Dec 22 2011 Kazuhisa Hara <kazuhisya@gmail.com>
- Update ruby version to 1.9.3-p0
* Wed Sep 21 2011 Chris MacLeod <stick@miscellaneous.net>
- break out into separate packages
* Mon Aug 29 2011 Gregory Graf <graf.gregory@gmail.com> - 1.9.2-p290
- Update ruby version to 1.9.2-p290
* Sat Jun 25 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p180-2
- Remove non-existant --sitearchdir and --vedorarchdir from %configure
- Replace --sitedir --vendordir with simpler --libdir
- Change %{_prefix}/share to %{_datadir}
* Tue Mar 7 2011 Robert Duncan <robert@robduncan.co.uk> - 1.9.2-p180-1
- Update prerequisites to include make
- Update ruby version to 1.9.2-p180
- Install /usr/share documentation
- (Hopefully!?) platform agnostic
* Sun Jan 2 2011 Ian Meyer <ianmmeyer@gmail.com> - 1.9.2-p136-1
- Initial spec to replace system ruby with 1.9.2-p136
