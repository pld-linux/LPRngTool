Summary:	LPRngTool - printer configuration, monitoring and management utility with GUI for LPRng
Summary(pl):	LPRngTool jest narzêdziem do monitorowania i zarz±dzania systemem druku LPRng
Name:		LPRngTool
Version:	1.2.7
Release:	1
License:	GPL
Group:		Applications/Publishing
Source0:	ftp://ftp.astart.com/pub/LPRng/LPRngTool/%{name}-%{version}.tgz
BuildRequires:	autoconf
BuildRequires:	automake
Requires:	ghostscript
Requires:	tcl
Requires:	tk >= 1.50
Requires:	LPRng >= 3.7
Requires:	ifhp >= 3.4
Obsoletes:	printtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_wmconfig	/etc/X11/wmconfig
%define		_controlpanel	/usr/lib/rhs/control-panel
%define		_filterdir	/usr/lib/filters
%define		_rhfilterdir	%{_filterdir}/rhs
%define		_prefix		/usr/X11R6

%description
LPRngTool is a printer configuration and print queue monitoring and
management utility with a graphical user interface. LPRngTool is
similar to Red Hat's 'printtool', but includes most of the additional
functions of LPRng (including printer pooling, printer redirection,
job accounting, etc), and the 'lpc' facilities for local and remote
queue management and monitoring. LPRngTool works with SMB, Windows, HP
JetDirect, locally-attached, and unfiltered printers and print queues.

%description -l pl
LPRngTool to narzêdzie do konfiguracji drukarki, monitorowania i
zarz±dzania kolejk± wydruku z graficznym interfejsem u¿ytkownika. Jest
podobne do RedHatowego printtoola, ale zwiera wiêkszo¶æ dodatkowych
funkcji LPRng (w tym przekierowanie drukarek, przydzielanie prac
itp.), oraz udogodnienia lpc do monitorowania i zarz±dzania lokalnymi
oraz zdalnymi kolejkami. LPRngTool dzia³a z drukarkami i kolejkami
SMB, Windows, HP JetDirect, lokalnie pod³±czonymi i niefiltrowanymi.

%prep
%setup -q

%build
#CFLAGS=%{rpmcflags} 
aclocal
autoconf
%configure \
	--with-lprngtool_conf=%{_sysconfdir}/lprngtool.conf \
	--with-printcap_path=%{_sysconfdir}/printcap \
	--with-spool_directory=/var/spool/lpd  \
	--with-ifhp_path=%{_filterdir}/ifhp \
	--with-filterdir=%{_filterdir} \
	--with-rhfilterdir=%{_rhfilterdir} \
	--with-gsupdir=%{_datadir}/ghostscript \
	--with-userid=lp \
	--with-groupid=lp 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_wmconfig},%{_bindir},%{_controlpanel},%{_filterdir}}
install -d $RPM_BUILD_ROOT{%{_rhfilterdir},%{_sysconfdir},%{_mandir},%{_mandir}/man1}

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install lprngtool.wmconfig $RPM_BUILD_ROOT%{_wmconfig}/lprngtool  
install lprngtool.init $RPM_BUILD_ROOT%{_controlpanel}/lprngtool.init
install lprngtool.xpm  $RPM_BUILD_ROOT%{_controlpanel}/lprngtool.xpm

gzip -9nf README CHANGES INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(0755,root,root) %{_bindir}/*
%{_controlpanel}/lprngtool.init
%{_controlpanel}/lprngtool.xpm
%attr(0644,root,root)   %config            %{_sysconfdir}/lprngtool.conf
%attr(0644,root,root)                      %{_sysconfdir}/lprngtool.conf.sample
%attr(0644,root,root)	%config(missingok) %{_wmconfig}/lprngtool
%{_mandir}/man1/*.1*
%dir %{_rhfilterdir}
%{_rhfilterdir}/*
