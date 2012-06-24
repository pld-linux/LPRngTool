Summary:	LPRngTool - printer configuration, monitoring and management utility with GUI for LPRng
Summary(pl):	LPRngTool - narz�dziem do monitorowania i zarz�dzania systemem druku LPRng
Name:		LPRngTool
Version:	1.3.2
Release:	4
License:	GPL
Group:		Applications/Publishing
Source0:	ftp://ftp.lprng.com/pub/LPRng/LPRngTool/%{name}-%{version}.tgz
# Source0-md5:	964bb358dbe140c7be5ebbdf0eecf64a
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-ac_fixes.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	samba-client
Requires:	LPRng >= 3.7
Requires:	ghostscript
Requires:	ifhp >= 3.4
Requires:	tcl
Requires:	tk >= 1.50
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	printtool

%define		_ifhpfilterdir	/usr/lib/lpfilters
%define		_filterdir	/usr/lib/filters

%description
LPRngTool is a printer configuration and print queue monitoring and
management utility with a graphical user interface. LPRngTool is
similar to Red Hat's 'printtool', but includes most of the additional
functions of LPRng (including printer pooling, printer redirection,
job accounting, etc), and the 'lpc' facilities for local and remote
queue management and monitoring. LPRngTool works with SMB, Windows, HP
JetDirect, locally-attached, and unfiltered printers and print queues.

%description -l pl
LPRngTool to narz�dzie do konfiguracji drukarki, monitorowania i
zarz�dzania kolejk� wydruku z graficznym interfejsem u�ytkownika. Jest
podobne do RedHatowego printtoola, ale zwiera wi�kszo�� dodatkowych
funkcji LPRng (w tym przekierowanie drukarek, przydzielanie prac
itp.), oraz udogodnienia lpc do monitorowania i zarz�dzania lokalnymi
oraz zdalnymi kolejkami. LPRngTool dzia�a z drukarkami i kolejkami
SMB, Windows, HP JetDirect, lokalnie pod��czonymi i niefiltrowanymi.

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.sub .
%configure \
	--with-lprngtool_conf=%{_sysconfdir}/lprngtool.conf \
	--with-printcap_path=%{_sysconfdir}/printcap \
	--with-spool_directory=/var/spool/lpd  \
	--with-ifhp_path=%{_ifhpfilterdir}/ifhp \
	--with-filterdir=%{_filterdir} \
	--with-gsupdir=%{_datadir}/ghostscript \
	--with-userid=lp \
	--with-groupid=lp
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
%attr(0755,root,root) %{_bindir}/*
%config %{_sysconfdir}/lprngtool.conf
%{_sysconfdir}/lprngtool.conf.sample
%{_mandir}/man1/*.1*
%dir %{_filterdir}
%attr(755,root,root) %{_filterdir}/atalkprint
%attr(755,root,root) %{_filterdir}/ncpprint
%attr(755,root,root) %{_filterdir}/smbprint
%{_filterdir}/printerdb
%{_filterdir}/testpage*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
