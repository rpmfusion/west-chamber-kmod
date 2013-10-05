# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels newest

%define svndate 20101017
%define svnver 105

Name:		west-chamber-kmod
Summary:	Kernel module (kmod) for west-chamber
Version:	0.0.1
Release:	7.%{?svndate}svn%{?dist}.52
License:	GPLv2+
Group:		System Environment/Kernel
URL:		http://code.google.com/p/scholarzhang/
#Source0:	http://scholarzhang.googlecode.com/files/west-chamber-%{version}.tar.gz
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r %{svnver} http://scholarzhang.googlecode.com/svn/trunk/west-chamber west-chamber-%{svndate}
#  tar -cjvf west-chamber-%{svndate}.tar.bz2 west-chamber-%{svndate}
Source0:	west-chamber-%{svndate}.tar.bz2
# Header files extracted from xtables-addons 1.30
Source1:	compat_xtables.h
Source2:	compat_skbuff.h
Source3:	compat_xtnu.h
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:	%{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
West-chamber is extensions named after the famous Chinese ancient friction - 
Romance of the West Chamber for iptables.

This package provides the west-chamber kernel modules. You must also install 
the west-chamber package in order to make use of these modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0

pushd west-chamber-%{svndate}
# do not build bundled xtables-addons modules
sed -i '/compat_xtables.o/d' extensions/Kbuild
sed -i '/build_ipset/d' extensions/Kbuild

# remove bundled files from xtables-addons
rm -rf include extensions/compat* 

cp -p %{SOURCE1} %{SOURCE2} %{SOURCE3} extensions/
popd

for kernel_version in %{?kernel_versions} ; do
	cp -a west-chamber-%{svndate} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
	export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
	make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" M=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
for kernel_version  in %{?kernel_versions} ; do
	install -dm 755 %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
	install -pm 755 _kmod_build_${kernel_version%%___*}/extensions/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done
%{?akmod_install}

%clean
rm -rf %{buildroot}

%changelog
* Sat Oct 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.52
- Rebuilt for kernel

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.51
- Rebuilt for kernel

* Sun Sep 29 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.50
- Rebuilt for kernel

* Sun Sep 29 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.49
- Rebuilt for kernel

* Sat Aug 31 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.48
- Rebuilt for kernel

* Thu Aug 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.47
- Rebuilt for kernel

* Fri Aug 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.46
- Rebuilt for kernel

* Tue Aug 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.45
- Rebuilt for kernel

* Sat Aug 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.44
- Rebuilt for kernel

* Tue Jul 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.43
- Rebuilt for kernel

* Mon Jul 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.42
- Rebuilt for kernel

* Sat Jul 06 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.41
- Rebuilt for kernel

* Sun Jun 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.40
- Rebuilt for kernel

* Mon Jun 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.39
- Rebuilt for kernel

* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.38
- Rebuilt for kernel

* Sat May 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.37
- Rebuilt for kernel

* Wed May 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.36
- Rebuilt for kernel

* Tue May 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.35
- Rebuilt for kernel

* Fri May 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.34
- Rebuilt for kernel

* Wed May 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.33
- Rebuilt for kernel

* Sun Apr 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.32
Rebuilt for kernel

* Thu Apr 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.31
- Rebuilt for kernel

* Thu Apr 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.30
- Rebuilt for kernel

* Sat Apr 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.29
- Rebuilt for kernel

* Wed Apr 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.28
- Rebuilt for kernel

* Tue Apr 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.27
- Rebuilt for kernel

* Fri Mar 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.26
- Rebuilt for kernel

* Mon Mar 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.25
- Rebuilt for kernel

* Fri Mar 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.24
- Rebuilt for kernel

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.23
Rebuilt for kernel

* Thu Feb 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.22
- Rebuilt for kernel

* Tue Feb 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.21
- Rebuilt for kernel

* Thu Feb 21 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.20
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.19
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.18
- Rebuilt for kernel

* Wed Feb 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.17
- Rebuilt for kernel

* Tue Feb 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.16
- Rebuilt for kernel

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.15
- Rebuilt for updated kernel

* Fri Jan 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.14
- Rebuilt for updated kernel

* Thu Jan 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.13
- Rebuilt for updated kernel

* Mon Jan 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.12
- Rebuilt for updated kernel

* Sun Jan 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.11
- Rebuilt for updated kernel

* Thu Jan 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.10
- Rebuilt for f18 final kernel

* Fri Dec 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.9
- Rebuilt for current f18 kernel

* Wed Dec 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.8
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.7
- Rebuilt for current f18 kernel

* Sun Nov 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.6
- Rebuilt for Fedora 18 Beta kernel

* Tue Feb 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.5
- Rebuild for UsrMove

* Wed Nov 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.4
- Rebuild for F-16 kernel

* Tue Nov 01 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.3
- Rebuild for F-16 kernel

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.2
- Rebuild for F-16 kernel

* Sun Oct 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.1
- Rebuild for F-16 kernel

* Sat May 28 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-7.20101017svn
- rebuild for F15 release kernel

* Thu Oct 28 2010 Chen Lei <supercyper@163.com> - 0.0.1-6.20101017svn
- Renew header files to work with xtables-addons >= 1.30

* Thu Aug 05 2010 Chen Lei <supercyper@163.com> - 0.0.1-5.20100405svn
- Renew header files to work with xtables-addons >= 1.27

* Fri Jun 18 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.8
- rebuild for new kernel

* Fri May 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.7
- rebuild for new kernel

* Thu May 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.6
- rebuild for new kernel

* Mon May 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.5
- rebuild for new kernel

* Fri May 07 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.4
- rebuild for new kernel

* Tue May 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.3
- rebuild for new kernel

* Thu Apr 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.2
- rebuild for new kernel

* Sun Apr 25 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.0.1-4.20100405svn.1
- rebuild for new kernel

* Thu Apr 15 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-4.20100405svn
- Changed 'buildforkernels' to current.

* Mon Apr 05 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-3.20100405svn
- svn 84

* Mon Mar 29 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-2.20100329svn
- svn 76

* Mon Mar 16 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-1
- Initial introduction.
