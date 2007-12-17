%define name aide
%define version 0.13
%define release %mkrel 1

Summary:     Advanced Intrusion Detection Environment
Name:        %{name}
Version:     %{version}
Release:     %{release}
Source0:     http://prdownloads.sourceforge.net/aide/%{name}-%{version}.tar.bz2
Source1:     %{name}.extra-0.7.tar.bz2
License:   GPL
URL:         http://sourceforge.net/projects/aide
Group:       Networking/Other
Buildrequires: flex glibc-devel glibc-static-devel
BuildRequires: libmhash-devel zlib-devel bison

%description

  AIDE (Advanced Intrusion Detection Environment) is a free replacement for
  Tripwire. It does the same things as the semi-free Tripwire and more.

  There are other free replacements available so why build a new one? All the
  other replacements do not achieve the level of Tripwire. And I wanted a
  program that would exceed the limitations of Tripwire.

  The idea is that for an intruder to get in, certain files on the system must
  change - configuration files, for example. And once an intruder is in, in
  order to do much useful, the intruder must gain root access - something else
  that requires changing files. aide ensures that you (root) can be notified of
  ANY changes to a configurable list of properties (modification date, size,
  various hash-values) of a configurable list files.

  Aide should be installed right after the OS installation, and before
  you have connected your system to a network (i.e., before any
  possibility exists that someone could alter files on your system).

%prep
    [ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != / ] \
    && rm -rf ${RPM_BUILD_ROOT}/

%setup -T -b 0
%setup -T -D -a 1

%configure 	--prefix=%{_prefix} \
			--sysconfdir=/etc \
            --with-config_file=/etc/aide.conf \
            --with-zlib \
            --with-mhash \
            --enable-mhash 

    grep -v "#define DEFAULT_DB" config.h                      > config.h.tmp
    echo '#define DEFAULT_DB "/var/lib/aide/aide.db"'         >> config.h.tmp
    echo '#define DEFAULT_DB_OUT "/var/lib/aide/aide.db.new"' >> config.h.tmp
    mv -f config.h.tmp config.h

%build
    make

%install
    mkdir -p ${RPM_BUILD_ROOT}/etc/cron.daily
    mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/sbin
    mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1 
    mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5 

    make prefix=$RPM_BUILD_ROOT%{_prefix} \
	 bindir=${RPM_BUILD_ROOT}%{_sbindir} \
	 mandir=${RPM_BUILD_ROOT}%{_mandir} \
	 install-strip

    mkdir -p -m 700 ${RPM_BUILD_ROOT}/var/lib/aide

    install -m 700 ./extra/aide.check $RPM_BUILD_ROOT/etc/cron.daily

    chmod 700 $RPM_BUILD_ROOT/var/lib/aide
    chmod 700 $RPM_BUILD_ROOT/usr/sbin/*

%post
    echo "****************************************************************"
    echo "* You should now set up an /etc/aide.conf to your              *"
    echo "* system and run '/usr/sbin/aide --init'                       *"
    echo "* (there is an example in /usr/share/doc/aide-0.9/aide.conf.in *"
    echo "*                                                              *"
    echo "* Then copy /etc/aide.conf, /usr/sbin/aide,                    *"
    echo "* and aide.db.new to a secure location                         *"
    echo "* (preferably read-only media)                                 *"
    echo "****************************************************************"

%clean
  [ -n "${RPM_BUILD_ROOT}" -a "${RPM_BUILD_ROOT}" != / ] \
  && rm -rf ${RPM_BUILD_ROOT}/

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README ./doc/manual.html ./extra/aide.html
%doc doc/aide.conf.in
%{_sbindir}/aide
%{_mandir}/man1/*
%{_mandir}/man5/*
/var/lib/aide
%defattr(0644,root,root,755)
%config(noreplace) /etc/cron.daily/aide.check


