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
Release:	7.%{?svndate}svn%{?dist}.72
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
chmod u+x %{buildroot}%{_prefix}/lib/modules/*/extra/*/*
%{?akmod_install}

%clean
rm -rf %{buildroot}

%changelog
* Wed Jun 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.72
- Rebuilt for kernel

* Sat May 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.71
- Rebuilt for kernel

* Sun May 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.70
- Rebuilt for kernel

* Thu May 09 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.69
Rebuilt for kernel

* Fri May 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.68
- Rebuilt for kernel

* Wed May 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.67
- Rebuilt for kernel

* Thu Apr 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.66
- Rebuilt for kernel

* Thu Apr 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.65
- Rebuilt for kernel

* Sat Apr 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.64
- Rebuilt for kernel

* Sun Mar 24 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.63
- Rebuilt for kernel

* Sat Mar 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.62
- Rebuilt for akmod

* Mon Mar 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.61
- Rebuilt for kernel

* Fri Mar 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.60
- Rebuilt for kernel

* Sun Mar 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.59
Rebuilt for kernel

* Sat Mar 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.58
- Rebuilt for kernel

* Tue Feb 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.57
- Rebuilt for kernel

* Tue Feb 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.56
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.55
- Rebuilt for kernel

* Sat Feb 16 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.54
- Rebuilt for kernel

* Tue Feb 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.53
- Rebuilt for kernel

* Mon Feb 04 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.52
- Rebuilt for akmod

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.51
- Rebuilt for akmod

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.50
- Rebuilt for updated kernel

* Fri Jan 25 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.49
- Rebuilt for updated kernel

* Sat Jan 19 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.48
- Rebuilt for updated kernel

* Thu Jan 17 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.47
- Rebuilt for updated kernel

* Wed Jan 09 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.46
- Rebuilt for updated kernel

* Sun Dec 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.45
- Rebuilt for updated kernel

* Sat Dec 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.44
- Rebuilt for updated kernel

* Tue Dec 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.43
- Rebuilt for updated kernel

* Wed Dec 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.42
- Rebuilt for updated kernel

* Wed Dec 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.41
- Rebuilt for updated kernel

* Wed Nov 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.40
- Rebuilt for updated kernel

* Wed Nov 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.39
- Rebuilt for updated kernel

* Tue Nov 20 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.38
- Rebuilt for updated kernel

* Thu Nov 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.37
- Rebuilt for updated kernel

* Thu Nov 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.36
- Rebuilt for updated kernel

* Tue Oct 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.35
- Rebuilt for updated kernel

* Thu Oct 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.34
- Rebuilt for updated kernel

* Thu Oct 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.33
- Rebuilt for updated kernel

* Mon Oct 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.32
- Rebuilt for updated kernel

* Wed Oct 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.31
- Rebuilt for updated kernel

* Thu Sep 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.30
- Rebuilt for updated kernel

* Mon Sep 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.29
- Rebuilt for updated kernel

* Fri Aug 31 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.28
- Rebuilt for updated kernel

* Wed Aug 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.27
- Rebuilt for updated kernel

* Thu Aug 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.26
- Rebuilt for updated kernel

* Sat Aug 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.25
- Rebuilt for updated kernel

* Tue Jul 31 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.24
- Rebuilt for updated kernel

* Sat Jul 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.23
- Rebuilt for updated kernel

* Tue Jul 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.22
- Rebuilt for updated kernel

* Fri Jul 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.21
- Rebuilt for updated kernel

* Thu Jun 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.20
- Rebuilt for updated kernel

* Thu Jun 21 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.19
- Rebuilt for updated kernel

* Sun Jun 17 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.18
- Rebuilt for updated kernel

* Tue Jun 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.17
- Rebuilt for updated kernel

* Sun May 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.16
- Rebuilt for updated kernel

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.15
- Rebuilt for release kernel

* Sun May 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.14
- Rebuilt for release kernel

* Wed May 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.13
- rebuild for updated kernel

* Sun May 06 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.12
- rebuild for updated kernel

* Sat May 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.11
- rebuild for updated kernel

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.10
- rebuild for updated kernel

* Sat Apr 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.9
- rebuild for updated kernel

* Sun Apr 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.8
- rebuild for updated kernel

* Mon Apr 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.7
- rebuild for updated kernel

* Thu Apr 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.0.1-7.20101017svn.6
- rebuild for beta kernel

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
