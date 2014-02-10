Summary:	Advanced Intrusion Detection Environment
Name:		aide
Version:	0.15.1
Release:	2
License:	GPLv2+
Group:		Monitoring
URL:		http://sourceforge.net/projects/aide
Source0:	http://prdownloads.sourceforge.net/aide/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/aide/%{name}-%{version}.tar.gz.asc
Source2:	aide.conf
Source3:	aidecheck
Source4:	aideupdate
Source5:	aideinit
Source6:	aideinit.8
#p0 sent upstream by kharec
Patch0:		aide-0.15-fix-str-fmt.patch
BuildRequires:	bison
Buildrequires:	flex
BuildRequires:	glibc-devel
BuildRequires:	glibc-static-devel
BuildRequires:	mhash-devel
BuildRequires:	pkgconfig(zlib)
Requires:	gnupg

%description
AIDE (Advanced Intrusion Detection Environment) is a free alternative to
Tripwire. It does the same things as the semi-free Tripwire and more. It
is a file system integrity monitoring tool.

%files
%doc AUTHORS COPYING ChangeLog NEWS README doc/aide.conf.in
%attr(0700,root,root) %{_sbindir}/aide
%attr(0700,root,root) %{_sbindir}/aidecheck
%attr(0700,root,root) %{_sbindir}/aideinit
%attr(0700,root,root) %{_sbindir}/aideupdate
%{_mandir}/man1/aide.1*
%{_mandir}/man5/aide.conf.5*
%{_mandir}/man8/aideinit.8*
%dir %attr(0700,root,root) /var/lib/aide
%dir %attr(0700,root,root) /var/lib/aide/reports
%attr(0700,root,root) %{_sysconfdir}/cron.daily/aide
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf

%post
echo "*********************************************************"
echo "* Please see aideinit(8) for information on how to setup"
echo "* AIDE+gpg which this AIDE implementation uses by default"
echo "*********************************************************"

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p0

%build
%configure2_5x \
	--with-config-file=%{_sysconfdir}/aide.conf \
	--with-zlib \
	--with-mhash \
	--with-syslog_facility=LOG_LOCAL1

perl -pi -e 's|/etc/aide.db|/var/lib/aide/aide.db|g' config.h

%make

%install
make prefix=%{buildroot}%{_prefix} \
	bindir=%{buildroot}%{_sbindir} \
	mandir=%{buildroot}%{_mandir} \
	install

mkdir -p %{buildroot}{/var/lib/aide/reports,%{_sysconfdir}/cron.daily,%{_mandir}/man8}

install -m 0600 %{SOURCE2} %{buildroot}%{_sysconfdir}/aide.conf
install -m 0700 %{SOURCE3} %{buildroot}%{_sbindir}/aidecheck
install -m 0700 %{SOURCE4} %{buildroot}%{_sbindir}/aideupdate
install -m 0700 %{SOURCE5} %{buildroot}%{_sbindir}/aideinit
install -m 0644 %{SOURCE6} %{buildroot}%{_mandir}/man8/aideinit.8
ln -sf ../..%{_sbindir}/aidecheck %{buildroot}%{_sysconfdir}/cron.daily/aide

