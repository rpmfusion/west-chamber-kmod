# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest
#define buildforkernels current
#define buildforkernels akmods

%define svndate 20100405
%define svnver 84

Name:		west-chamber-kmod
Summary:	Kernel module (kmod) for west-chamber
Version:	0.0.1
Release:	4.%{?svndate}svn%{?dist}.6
License:	GPLv2+
Group:		System Environment/Kernel
URL:		http://code.google.com/p/scholarzhang/
#Source0:	http://scholarzhang.googlecode.com/files/west-chamber-%{version}.tar.gz
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
#  svn export -r %{svnver} http://scholarzhang.googlecode.com/svn/trunk/west-chamber west-chamber-%{svndate}
#  tar -cjvf west-chamber-%{svndate}.tar.bz2 west-chamber-%{svndate}
Source0:	west-chamber-%{svndate}.tar.bz2
Source11:	west-chamber-kmodtool-excludekernel-filterfile
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:	%{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
West-chamber is extensions named after the famous Chinese ancient friction - 
Romance of the West Chamber for iptables.

This package provides the west-chamber kernel modules. You must also install 
the west-chamber package in order to make use of these modules.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -c -T -a 0
#do not build bundled xtables-addons modules
pushd west-chamber-%{svndate}
sed -i '/compat_xtables.o/d' extensions/Kbuild
sed -i '/build_ipset/d' extensions/Kbuild
popd
for kernel_version in %{?kernel_versions} ; do
	cp -a west-chamber-%{svndate} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
	export XA_ABSTOPSRCDIR=${PWD}/_kmod_build_${kernel_version%%___*}
	make %{?_smp_mflags} V=1 -C "${kernel_version##*___}" SUBDIRS=${PWD}/_kmod_build_${kernel_version%%___*}/extensions modules
done


%install
rm -rf %{buildroot}
for kernel_version  in %{?kernel_versions} ; do
	find _kmod_build_${kernel_version%%___*}/extensions -name "*.ko" -exec mv {} _kmod_build_${kernel_version%%___*}/extensions ";"
	install -dm 755 %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
	install -pm 755 _kmod_build_${kernel_version%%___*}/extensions/*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}
done
chmod u+x %{buildroot}/lib/modules/*/extra/*/*
%{?akmod_install}

%clean
rm -rf %{buildroot}


%changelog
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

* Thu Apr 15 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-4.20100405svn-- Changed 'buildforkernels' to current.

* Mon Apr 05 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-3.20100405svn
- svn 84

* Mon Mar 29 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-2.20100329svn
- svn 76

* Mon Mar 16 2010 Caius 'kaio' Chance <kaio at fedoraproject.org> - 0.0.1-1
- Initial introduction.
