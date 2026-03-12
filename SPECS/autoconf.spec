%global package_speccommit 02a344c7d0fd5e2a3bb5e0c786877652de200b71
%global usver 2.71
%global xsver 2
%global xsrel %{xsver}%{?xscount}%{?xshash}
# Enable Emacs support
%bcond_with autoconf_enables_emacs
# Run extended test
%bcond_without autoconf_enables_optional_test

Summary:    A GNU tool for automatically configuring source code
Name:       autoconf
Version:    2.71
Release: %{?xsrel}%{?dist}
License:    GPLv2+ and GFDL
Source0: autoconf-2.71.tar.xz
Source1: config.site
Source2: autoconf-init.el
Patch0: 0001-_AC_PROG_CXX_STDCXX_EDITION_TRY-fix-typo-in-variable.patch
Patch1: 0001-Fix-testsuite-failures-with-bash-5.2.patch
URL:        https://www.gnu.org/software/autoconf/

# Cherry-pick from upstream f460883035ef849a2248b1713f711292ec19f4f0
# Cherry-pick from upstream 412166e185c00d6eacbe67dfcb0326f622ec4020

BuildArch:  noarch


# run "make check" by default
%bcond_without check

# m4 >= 1.4.6 is required, >= 1.4.14 is recommended:
BuildRequires:      perl
Requires:           perl(File::Compare)
Requires:           perl-interpreter
BuildRequires:      m4 >= 1.4.14
Requires:           m4 >= 1.4.14
%if %{with autoconf_enables_emacs}
Requires:           emacs-filesystem
BuildRequires:      emacs
%endif
# the filtering macros are currently in /etc/rpm/macros.perl:
BuildRequires:      perl-generators
BuildRequires:      perl-macros
BuildRequires:      perl(Data::Dumper)
# from f19, Text::ParseWords is not the part of 'perl' package
BuildRequires:      perl(Text::ParseWords)

BuildRequires:      make

%if %{with check}
%if %{with autoconf_enables_optional_test}
# For extended testsuite coverage
BuildRequires:      gcc-gfortran
%if 0%{?fedora} >= 15
BuildRequires:      erlang
%endif
%endif
%endif

# filter out bogus perl(Autom4te*) dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Autom4te::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Autom4te::

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.


%prep
%autosetup -p1

%build
%if %{with autoconf_enables_emacs}
export EMACS=%{_bindir}/emacs
%else
export EMACS=%{_bindir}/false
%endif
%configure \
    %{?with_autoconf_enables_emacs:--with-lispdir=%{_emacs_sitelispdir}/autoconf}
%make_build


%check
%if %{with check}
# make check # TESTSUITEFLAGS='1-198 200-' # will disable nr. 199.
# make check TESTSUITEFLAGS="-k \!erlang"
make check %{?_smp_mflags}
%endif


%install
%make_install
mkdir -p %{buildroot}/share
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}

%if %{with autoconf_enables_emacs}
# Create file to activate Emacs modes as required
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_emacs_sitestartdir}
%endif

%files
%license COPYING*
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
# don't include info's TOP directory
%exclude %{_infodir}/dir
%{_datadir}/autoconf/
%{_datadir}/config.site
%if %{with autoconf_enables_emacs}
%{_datadir}/emacs/site-lisp/*
%endif
%{_mandir}/man1/*
%doc AUTHORS ChangeLog NEWS README THANKS TODO


%changelog
* Wed Jan 08 2025 Alex Brett <alex.brett@cloud.com> - 2.71-2
- CA-404468: Remove dependency on help2man

* Tue Jul 11 2023 Tim Smith <tim.smith@citrix.com> - 2.71-1
- First imported release

