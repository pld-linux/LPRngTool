Summary:	LPRngTool is a printer configuration and print queue monitoring and management utility with a graphical user interface for LPRng.
Summary(pl):	LPRngTool jest narzêdziem do monitorowania i zarz±dzania systemem druku LPRng
Name:		LPRngTool
Version:	1.2.7
Release:	1
License:	GPL
Group:		Applications/Publishing
Group(de):	Applikationen/Publizieren
Group(es):	Aplicaciones/Editoración
Group(pl):	Aplikacje/Publikowanie
Group(pt_BR):	Aplicações/Editoração
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

%define wmconfig /etc/X11/wmconfig
%define controlpanel /usr/lib/rhs/control-panel
%define filterdir /usr/libexec/filters
%define rhfilterdir %{filterdir}/rhs

%description
LPRngTool is a printer configuration and print queue monitoring and
management utility with a graphical user interface. LPRngTool is
similar to Red Hat's 'printtool', but includes most of the additional
functions of LPRng (including printer pooling, printer redirection,
job accounting, etc), and the 'lpc' facilities for local and remote
queue management and monitoring. LPRngTool works with SMB, Windows, HP
JetDirect, locally-attached, and unfiltered printers and print queues.

%prep
%setup -q

%build
#CFLAGS=%{rpmcflags} 
aclocal
autoconf
%configure \
	--with-lprngtool_conf=%{sysconfdir}/lprngtool.conf \
	--with-printcap_path=%{sysconfdir}/printcap \
	--with-spool_directory=/var/spool/lpd  \
	--with-ifhp_path=%{filterdir}/ifhp \
	--with-filterdir=%{filterdir} \
	--with-rhfilterdir=%{rhfilterdir} \
	--with-gsupdir=%{datadir}/ghostscript \
	--with-userid=lp \
	--with-groupid=lp 
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
install -d $RPM_BUILD_ROOT/%wmconfig
install -d $RPM_BUILD_ROOT/%bindir
install -d $RPM_BUILD_ROOT/%controlpanel
install -d $RPM_BUILD_ROOT/%filterdir
install -d $RPM_BUILD_ROOT/%rhfilterdir
install -d $RPM_BUILD_ROOT/%sysconfdir
rm -rf $RPM_BUILD_ROOT/%mandir/man1
install -d $RPM_BUILD_ROOT/%mandir/man1

%{__make} DESTDIR=$RPM_BUILD_ROOT install

install lprngtool.wmconfig $RPM_BUILD_ROOT/%wmconfig/lprngtool  
install lprngtool.init $RPM_BUILD_ROOT/%controlpanel/lprngtool.init
install lprngtool.xpm  $RPM_BUILD_ROOT/%controlpanel/lprngtool.xpm

gzip -nf9 README CHANGES INSTALL

%clean

%files
%defattr(644,root,root,755)
%doc *.gz
%{bindir}/*
%{controlpanel}/lprngtool.init
%{controlpanel}/lprngtool.xpm
%attr(0644,root,root)   %config            %{sysconfdir}/lprngtool.conf
%attr(0644,root,root)                      %{sysconfdir}/lprngtool.conf.sample
%attr(0644,root,root)	%config(missingok) %{wmconfig}/lprngtool
%{mandir}/man1/*.1*
%dir %rhfilterdir
%{rhfilterdir}/*
