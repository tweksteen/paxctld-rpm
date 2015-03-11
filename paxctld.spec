Name: paxctld
Version: 1.0
Release: 1%{?dist}
Summary: PaX flags maintenance daemon
Group: admin
License: GPLv2
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
URL: https://grsecurity.net
Source: https://grsecurity.net/paxctld-1.0.tgz
Patch: paxctld-systemd.patch

%description
paxctld is a daemon that automatically applies PaX flags to binaries on
the system.  These flags are applied via user extended attributes and are
refreshed on any update to the binaries specified in its configuration file.

%prep
%setup -q
%patch -p1

%build
make %{?_smp_mflags}

%install
%make_install
install -d $RPM_BUILD_ROOT/etc/systemd/system
install -m755 rpm/paxctld.service $RPM_BUILD_ROOT/etc/systemd/system

%post
/sbin/systemctl enable paxctld.service >/dev/null 2>&1 || :

%preun
%systemd_preun paxctld.service

%postun
%systemd_postun paxctld.service

%files
%defattr(-,root,root)
%attr(0755,root,root) /sbin/paxctld
%attr(0644,root,root) %{_mandir}/man8/paxctld.8.gz
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/paxctld.conf
%attr(0755,root,root) %config %{_sysconfdir}/systemd/system/paxctld.service
%doc

%changelog
* Wed Dec 17 2014 Brad Spengler <spender@grsecurity.net> 1.0
- Initial release
