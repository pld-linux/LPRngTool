Summary:	LPRngTool - printer configuration, monitoring and management utility with GUI for LPRng
Summary(pl.UTF-8):	LPRngTool - narzędziem do monitorowania i zarządzania systemem druku LPRng
Name:		LPRngTool
Version:	1.3.2
Release:	4
License:	GPL v2
Group:		Applications/Publishing
Source0:	http://www.lprng.com/DISTRIB/LPRngTool/%{name}-%{version}.tgz
# Source0-md5:	964bb358dbe140c7be5ebbdf0eecf64a
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-ac_fixes.patch
URL:		http://www.lprng.com/LPRngTool.html
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	LPRng >= 3.7
Requires:	ghostscript
Requires:	ifhp >= 3.4
Requires:	tcl >= 8.3
Requires:	tk >= 8.3
# or mpage, selectable at configure time (see configure)
Suggests:	a2ps
Suggests:	samba-client
# ncpfs (/usr/bin/nprint) for Netware printing, but it's probably too legacy to suggest these days
# pap? (see configure)
Obsoletes:	printtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		lpfiltersdir	%{_libdir}/lpfilters

%description
LPRngTool is a printer configuration and print queue monitoring and
management utility with a graphical user interface. LPRngTool is
similar to Red Hat's 'printtool', but includes most of the additional
functions of LPRng (including printer pooling, printer redirection,
job accounting, etc), and the 'lpc' facilities for local and remote
queue management and monitoring. LPRngTool works with SMB, Windows, HP
JetDirect, locally-attached, and unfiltered printers and print queues.

%description -l pl.UTF-8
LPRngTool to narzędzie do konfiguracji drukarki, monitorowania i
zarządzania kolejką wydruku z graficznym interfejsem użytkownika. Jest
podobne do RedHatowego printtoola, ale zwiera większość dodatkowych
funkcji LPRng (w tym przekierowanie drukarek, przydzielanie prac
itp.), oraz udogodnienia lpc do monitorowania i zarządzania lokalnymi
oraz zdalnymi kolejkami. LPRngTool działa z drukarkami i kolejkami
SMB, Windows, HP JetDirect, lokalnie podłączonymi i niefiltrowanymi.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.sub .
%configure \
	A2PS=/usr/bin/a2ps \
	GS=/usr/bin/gs \
	NPRINT=/usr/bin/nprint \
	SMBCLIENT=/usr/bin/smbclient \
	WITH=/usr/bin/wish \
	--with-filterdir=%{lpfiltersdir} \
	--with-ifhp_path=%{lpfiltersdir} \
	--with-gsupdir=%{_datadir}/ghostscript \
	--with-lprngtool_conf=%{_sysconfdir}/lprngtool.conf \
	--with-printcap_path=%{_sysconfdir}/printcap \
	--with-spool_directory=/var/spool/lpd  \
	--with-groupid=lp \
	--with-userid=lp
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_filterdir}} \
	$RPM_BUILD_ROOT{%{_sysconfdir},%{_mandir},%{_mandir}/man1} \
	$RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES
%attr(755,root,root) %{_bindir}/lprngtool
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lprngtool.conf
%{_sysconfdir}/lprngtool.conf.sample
%dir %{lpfiltersdir}
%attr(755,root,root) %{lpfiltersdir}/atalkprint
%attr(755,root,root) %{lpfiltersdir}/ncpprint
%attr(755,root,root) %{lpfiltersdir}/smbprint
%{lpfiltersdir}/printerdb
%{lpfiltersdir}/testpage*
%{_desktopdir}/LPRngTool.desktop
%{_pixmapsdir}/LPRngTool.png
%{_mandir}/man1/lprngtool.1*
