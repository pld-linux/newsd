# TODO
# - run as 'news' user
# - pldize initscript
Summary:	newsd usenet news server
Name:		newsd
Version:	1.44
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://ftp.funet.fi/pub/mirrors/ftp.easysw.com/pub/newsd/%{version}/%{name}-%{version}-source.tar.bz2
# Source0-md5:	74081b4a51ac94a250f21953eca83ee9
URL:		http://www.easysw.com/~mike/newsd/
BuildRequires:	libstdc++-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Newsd is a standalone local NNTP news server for private newsgroup
serving on a single server. It is useful for serving private
newsgroup(s) to an intranet or the Internet and can act as a simple
mail gateway, however it does not interface with other news servers
and cannot manage distributed news feeds, i.e. Usenet news.

%prep
%setup -q

%build
%configure
%{__make} \
	OPTIM=""

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	initdir="" \
	INSTALL_BIN=install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/newsd
install newsd.sh $RPM_BUILD_ROOT/etc/rc.d/init.d/newsd

rm -rf $RPM_BUILD_ROOT%{_mandir}/cat*
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%doc inn2newsd.sh
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/newsd.conf
%attr(754,root,root) /etc/rc.d/init.d/newsd
%attr(755,root,root) %{_sbindir}/newsd
%{_mandir}/man5/newsd.conf.5*
%{_mandir}/man8/newsd.8*

%dir /var/spool/newsd
