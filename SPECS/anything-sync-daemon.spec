Name:              anything-sync-daemon
Version:           5.76
Release:           1%{?dist}
Summary:           Offload any directories to RAM for speed and wear reduction
License:           MIT
URL:               https://github.com/graysky2/anything-sync-daemon 
Source0:           https://github.com/graysky2/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:         noarch
BuildRequires:     systemd
Requires:          rsync
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd

%description
Symlinks and syncs arbitrary directories to RAM via tmpfs which will reduce
HDD/SDD calls.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
make install-systemd-all DESTDIR=%{buildroot}

%post
if [ $1 -eq 1 ]; then 
 setsebool -P rsync_full_access 1 >/dev/null 2>&1 || :
fi
%systemd_post asd.service

%preun
if [ $1 -eq 0 ]; then
 setsebool -P rsync_full_access 0 >/dev/null 2>&1 || :
fi
%systemd_preun asd.service

%postun
%systemd_postun_with_restart asd.service

%files
%doc README* MIT
%config(noreplace) %{_sysconfdir}/asd.conf
%{_bindir}/*
%{_mandir}/man1/*.1*
%{_unitdir}/asd*.*
%{_prefix}/share/bash-completion/completions/asd
%{_prefix}/share/zsh/site-functions/_asd

%changelog
* Sun Nov 29 2015 Steven Merrill <steven.merrill@gmail.com> - 5.76-1
- Bump asd version, install bash/zsh completion.

* Sat Jan 24 2015 Steven Merrill <steven.merrill@gmail.com> - 5.65-1
- Initial RPM release
