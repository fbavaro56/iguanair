# determine the python version
%define pyver %(python -V 2>&1 | sed 's/Python \\(.\\..\\).*/\\1/')
%define version %(head -n 1 ../ChangeLog | sed 's/.*(\\(.*\\)).*/\\1/')

Name:           iguanaIR
Version:        %{version}
Release:        1
Summary:        Driver for Iguanaworks USB IR transceiver.

Group:          System Environment/Daemons
License:        GPL
URL:            http://iguanaworks.net/ir
Source0:        http://iguanaworks.net/ir/releases/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:         lirc >= 0.8.1 libusb1
Requires(post):   /usr/bin/install /sbin/chkconfig
Requires(pre):    /usr/sbin/useradd
Requires(preun):  /sbin/chkconfig /sbin/service /bin/rmdir
Requires(postun): /usr/sbin/userdel
BuildRequires:    cmake libusb1-devel

%description
This package provides igdaemon and igclient, the programs necessary to
control the Iguanaworks USB IR transceiver.  The header files needed
to interact with igdaemon are also included.

%package python
Group: System Environment/Daemons
Summary: Python module for Iguanaworks USB IR transceiver.
Requires: python >= 2.4 iguanaIR = %{version}
BuildRequires: python-devel swig

%description python
This package provides the swig-generated Python module for interfacing
with the Iguanaworks USB IR transceiver.

%package reflasher
Group: System Environment/Daemons
Summary: Reflasher for Iguanaworks USB IR transceiver.
Requires: iguanaIR-python = %{version}
BuildArch: noarch

%description reflasher
This package provides the reflasher/testing script and assorted firmware versions for the Iguanaworks USB IR transceiver.  If you have no idea what this means, you don't need it.

%prep
%setup -q

%build
mkdir -p build
cd build
cmake -DLIBDIR=%{_libdir} ..
cd ..
make -C build %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make -C build install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

# must create the user and group before files are put down
%pre
#TODO: stupid to not support the long versions
# TODO: do NOT specify the uid!
/usr/sbin/useradd -u 213 -c "Iguanaworks IR Daemon" -d / -s /sbin/nologin iguanair 2>/dev/null || true
#/usr/sbin/useradd --uid %{uid} --comment "Iguanaworks IR Daemon" --home / --shell /sbin/nologin iguanair 2>/dev/null || true

# must add the service after the files are placed
%post
/sbin/chkconfig --add %{name}

# before the files are removed stop the service
%preun
if [ $1 = 0 ]; then
  /sbin/service %{name} stop > /dev/null 2>&1 || true
  /sbin/chkconfig --del %{name}
fi

# after the files are removed nuke the user and group
%postun
if [ $1 = 0 ]; then
  /usr/sbin/userdel iguanair
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE LICENSE-LGPL WHY README.txt ChangeLog examples
/usr/bin/igclient
/usr/bin/igdaemon
%{_libdir}/lib%{name}.so*
%{_libdir}/%{name}
/etc/init.d/%{name}
# makes .rpmsave
%config /etc/default/%{name}
# makes .rpmnew
#%config(noreplace) /etc/default/%{name}
/lib/udev/rules.d/80-%{name}.rules
/usr/include/%{name}.h

%files python
%{_libdir}/python%{pyver}/site-packages/*

%files reflasher
/usr/share/%{name}-reflasher
/usr/bin/%{name}-reflasher

%changelog
* Sat Nov 20 2010 Joseph Dunn <jdunn@iguanaworks.net> 1.0-1
- Significant release to try and get back on track.

* Sat Jun 27 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.96-1
- Bug fix release.

* Fri Mar 27 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.95-1
- Decided to do another release to fix a udev problem.

* Sun Mar 23 2008 Joseph Dunn <jdunn@iguanaworks.net> 0.94-1
- Better windows support, a pile of bugs fixed.  Works with newer
  firmwares (version 0x102) including frequency and channel support
  with or without LIRC.

* Sat Mar 10 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.31-1
- First release with tentative win32 and darwin support.  Darwin needs
  some work, and windows needs to interface with applications.

* Thu Feb 1 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.30-1
- Added a utility to change the frequency on firmware version 3, and
  had to make iguanaRemoveData accessible to python code.

* Sun Jan 21 2007 Joseph Dunn <jdunn@iguanaworks.net> 0.29-1
- Last currently known problem in the driver.  Using clock_gettime
  instead of gettimeofday to avoid clock rollbacks.

* Sun Dec 31 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.26-1
- Happy New Years! and a bugfix.  Long standing bug that caused the
  igdaemon to hang is fixed.

* Sun Dec 10 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.25-1
- The socket specification accept a path instead of just an index or
  label.

* Wed Dec 6 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.24-1
- Fixes bad argument parsing in igdaemon, and the init script *should*
  work for fedora and debian now.

* Wed Oct 18 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.19-1
- A real release has been made, and we'll try to keep track of version
  numbers a bit better now.

* Sat Sep 23 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.10-1
- Preparing for a real release.

* Wed Jul 11 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.9-1
- Switch to using udev instead of hotplug.

* Mon Jul 10 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.8-1
- Version number bumps, and added python support and package.

* Mon Mar 27 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.5-1
- Version number bump.

* Mon Mar 20 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.4-1
- Version number bump.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.3-1
- Packaged a client library, and header file.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.2-2
- Added support for chkconfig

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.2-1
- Added files for hotplug.

* Tue Mar 07 2006 Joseph Dunn <jdunn@iguanaworks.net> 0.1-1
- Initial RPM spec file.
