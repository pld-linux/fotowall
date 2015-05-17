Summary:	Photo collection creativity tool
Name:		fotowall
Version:	0.9
Release:	1
License:	GPL v2+
Group:		Applications/Multimedia
Source0:	http://fotowall.googlecode.com/files/Fotowall-%{version}.tar.bz2
# Source0-md5:	142ef697332e0777c6d22c5bc96cc438
URL:		http://www.enricoros.com/opensource/fotowall/
BuildRequires:	QtCore-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtGui-devel
BuildRequires:	QtNetwork-devel
BuildRequires:	QtOpenGL-devel
BuildRequires:	QtSvg-devel
BuildRequires:	QtXml-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libv4l-devel
BuildRequires:	qt4-build
BuildRequires:	qt4-qmake
BuildRequires:	rpmbuild(macros) >= 1.596
Requires:	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FotoWall is a creative tool that allows you to layout your photos or
pictures in a personal way. You can add pictures, then resize, move,
change colors, text, shadows, etc..

%prep
%setup -q -n Fotowall-%{version}

# for hidden-file-or-dir warning
sed -i -e "s/\.build/build/" %{name}.pro
# Unused file
sed -i -e "/scripts/d" -e "s@man\ \\\@man@" %{name}.pro
# for v4l1 compatibility
sed -i -e 's/linux\/videodev.h/libv4l1-videodev.h/' 3rdparty/videocapture/VideoDevice.h

%build
qmake-qt4
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

desktop-file-install --vendor="" --dir $RPM_BUILD_ROOT%{_desktopdir} \
  $RPM_BUILD_ROOT/%{_desktopdir}/%{name}.desktop

# PLD appstream-util too old(?) for replace-screenshots action
%if 0
# Update the screenshot shown in the software center
#
# NOTE: It would be *awesome* if this file was pushed upstream.
#
# See http://people.freedesktop.org/~hughsient/appdata/#screenshots for more details.
#
appstream-util replace-screenshots $RPM_BUILD_ROOT%{_datadir}/appdata/fotowall.appdata.xml \
  https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/fotowall/a.png
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database

%postun
%update_desktop_database

%files
%defattr(644,root,root,755)
%doc GPL_V2 README.markdown
%attr(755,root,root) %{_bindir}/%{name}
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
%{_mandir}/man1/%{name}.1*
