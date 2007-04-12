%define _appsdir %{_libdir}/apps

Summary:	A collection of ROX Wrapper scripts.
Name:		rox-wrappers
Version:	0.1
Release:	4mdk
Group:		Graphical desktop/Other
License:	GPL
URL:		http://rox.sourceforge.net
Source0:	Wrappers.tar.bz2
Source1:	Drives.tar.bz2
Source2:	Antiword.tar.bz2
Source3:	Display.tar.bz2
Source4:	LaTeX.tar.bz2
Source5:	XDvi.tar.bz2
Source6:	XEmacs.tar.bz2
Source7:	XV.tar.bz2
Source8:	xTerminal.tar.bz2
Source9:	roxstuff.tar.bz2
Source10:	appmenu_convert.pl.bz2
Patch0:		Wrappers-AppRun-patch
Patch1:		Antiword-AppRun-patch
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  ImageMagick
BuildArchitectures: noarch

%description
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for various 
applications.

#
# Multimedia
%package multimedia
Summary:  A collection of ROX Wrapper scripts for multimedia applications.
Group:	  Graphical desktop/Other
Requires: rox

%description multimedia
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for multimedia 
applications.


#
# Networking
%package networking
Summary:  A collection of ROX Wrapper scripts for networking applications.
Group:	  Graphical desktop/Other
Requires: rox


%description networking
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for networking 
applications.


#
# Office
%package office
Summary:  A collection of ROX Wrapper scripts for office applications.
Group:	  Graphical desktop/Other
Requires: rox

%description office
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for office 
applications.


#
# Text tools
%package texttools
Summary:  A collection of ROX Wrapper scripts for text editors/viewers.
Group:	  Graphical desktop/Other
Requires: rox

%description texttools
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for text 
editors/viewers.


#
# Utilities
%package utils
Summary:  A collection of ROX Wrapper scripts for various utilities.
Group:	  Graphical desktop/Other
Requires: rox

%description utils
ROX-Filer is a fast, powerful, and easy to use graphical file
manager. It has full support for drag-and-drop and application
directories.  The filer can also provide a pinboard (allowing you to pin
up files on your desktop background) and panels.  The emphasis is on
uncluttered directory views; menus and prompts only appear when needed.

This package contains a collection of ROX wrapper scripts for various 
utilities.


%prep
%setup -q -T -b 0 -c -n %{name}-%{version}
%setup -q -T -D -a 1 -n %{name}-%{version}
%setup -q -T -D -a 2 -n %{name}-%{version}
%setup -q -T -D -a 3 -n %{name}-%{version}
%setup -q -T -D -a 4 -n %{name}-%{version}
%setup -q -T -D -a 5 -n %{name}-%{version}
%setup -q -T -D -a 6 -n %{name}-%{version}
%setup -q -T -D -a 7 -n %{name}-%{version}
%setup -q -T -D -a 8 -n %{name}-%{version}
%setup -q -T -D -a 9 -n %{name}-%{version}

# Editors nedit patch
%patch0 -p1

# Antiword ggv patch
%patch1 -p1

# Fix path for antiword
for FILE in Antiword/AppRun Antiword/Convert ; do

    sed "s|\$APP_DIR/\$PLATFORM|%{_bindir}|" < $FILE > $FILE.tmp
    mv $FILE.tmp $FILE
    chmod 755 $FILE

done

%build

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_appsdir}

cp -rf Wrappers/* ${RPM_BUILD_ROOT}%{_appsdir}
cp -rf Drives/* ${RPM_BUILD_ROOT}%{_appsdir}
rm -f  XEmacs/AppRun.ksh
mv -f  roxstuff/Floppy roxstuff/Floppy-2
mv -f  roxstuff/XEmacs roxstuff/XEmacs-2
cp -rf roxstuff/* ${RPM_BUILD_ROOT}%{_appsdir}



for DIR in Antiword Display LaTeX XDvi XEmacs XV xTerminal ; do

    mkdir -p ${RPM_BUILD_ROOT}%{_appsdir}/$DIR
    cp -rf $DIR/* ${RPM_BUILD_ROOT}%{_appsdir}/$DIR

done

rm -rf ${RPM_BUILD_ROOT}%{_appsdir}/Antiword/src

function copy_dotfiles {

    for FILE in */.DirIcon* ; do

	if [ -e "$FILE" ]; then

	    install -m 644 "$FILE" "${RPM_BUILD_ROOT}%{_appsdir}/$FILE"

	else

	    true

	fi

    done

}

for DIR in Drives Wrappers roxstuff ; do

    cd "$DIR"
    copy_dotfiles
    cd ../

done

for DIR in ${RPM_BUILD_ROOT}%{_appsdir}/*/ ; do

    # Convert xpm to png.
    if [ -e $DIR/AppIcon.xpm ]; then

	convert $DIR/AppIcon.xpm $DIR/AppIcon.png
	mv $DIR/AppIcon.png $DIR/.DirIcon
	rm -f $DIR/AppIcon.xpm

    fi

    # Convert old AppMenu to new AppInfo.xml (doesn't work).
    if [ -e $DIR/AppMenu ]; then

	#bzcat %{SOURCE10} > appmenu_convert.pl
	#chmod 755 ./appmenu_convert.pl
	#./appmenu_convert.pl $DIR/AppMenu > $DIR/AppInfo.xml

	#Remove old AppMenu files
	rm -f $DIR/AppMenu

    fi

done

install -m 644 Antiword/.DirIcon* ${RPM_BUILD_ROOT}%{_appsdir}/Antiword/.DirIcon
mv -f ${RPM_BUILD_ROOT}%{_appsdir}/XEmacs/ChangeLog ${RPM_BUILD_ROOT}%{_appsdir}/XEmacs/Help/ChangeLog
mv ${RPM_BUILD_ROOT}%{_appsdir}/CD-ROM ${RPM_BUILD_ROOT}%{_appsdir}/"Samba CD-ROM"
mv ${RPM_BUILD_ROOT}%{_appsdir}/"CD Writer" ${RPM_BUILD_ROOT}%{_appsdir}/"Samba CD-Writer"

# Don't step on MDK rox package.
mv ${RPM_BUILD_ROOT}%{_appsdir}/Gimp ${RPM_BUILD_ROOT}%{_appsdir}/Gimp-2
mv ${RPM_BUILD_ROOT}%{_appsdir}/Vim ${RPM_BUILD_ROOT}%{_appsdir}/Vim-2

# Fix permissions
chmod -R u=rwX %{buildroot}%{_appsdir}
chmod -R go=rX %{buildroot}%{_appsdir}

%clean
rm -rf ${RPM_BUILD_ROOT}


#
# Multimedia
%files multimedia
%defattr (-,root,root)

%dir %{_appsdir}/Audio
%{_appsdir}/Audio/*
%{_appsdir}/Audio/.DirIcon

%dir %{_appsdir}/Display
%{_appsdir}/Display/*
%{_appsdir}/Display/.DirIcon

%dir %{_appsdir}/Gimp-2
%{_appsdir}/Gimp-2/*
%{_appsdir}/Gimp-2/.DirIcon

%dir %{_appsdir}/Graphics
%{_appsdir}/Graphics/*
%{_appsdir}/Graphics/.DirIcon

%dir %{_appsdir}/XFig
%{_appsdir}/XFig/*
%{_appsdir}/XFig/.DirIcon

%dir %{_appsdir}/XV
%{_appsdir}/XV/*
%{_appsdir}/XV/.DirIcon


#
# Networking
%files networking
%defattr (-,root,root)

%dir %{_appsdir}/Browser
%{_appsdir}/Browser/*
%{_appsdir}/Browser/.DirIcon

%dir "%{_appsdir}/Samba CD-ROM"
"%{_appsdir}/Samba CD-ROM/"

%dir "%{_appsdir}/Samba CD-Writer"
"%{_appsdir}/Samba CD-Writer/"


#
# Office
%files office
%defattr (-,root,root)

%dir %{_appsdir}/PIM
%{_appsdir}/PIM/*
%{_appsdir}/PIM/.DirIcon


#
# Text Tools
%files texttools
%defattr (-,root,root)

%dir %{_appsdir}/Antiword
%{_appsdir}/Antiword/*
%{_appsdir}/Antiword/.DirIcon

%dir %{_appsdir}/Editors
%{_appsdir}/Editors/*
%{_appsdir}/Editors/.DirIcon

%dir %{_appsdir}/LaTeX
%{_appsdir}/LaTeX/*
%{_appsdir}/LaTeX/.DirIcon

%dir %{_appsdir}/Vim-2
%{_appsdir}/Vim-2/*
%{_appsdir}/Vim-2/.DirIcon

%dir %{_appsdir}/XDvi
%{_appsdir}/XDvi/*
%{_appsdir}/XDvi/.DirIcon

%dir %{_appsdir}/XEmacs
%{_appsdir}/XEmacs/*
%{_appsdir}/XEmacs/.DirIcon

%dir %{_appsdir}/XEmacs-2
%{_appsdir}/XEmacs-2/*
%{_appsdir}/XEmacs-2/.DirIcon


#
# Utilities
%files utils
%defattr (-,root,root)

%dir %{_appsdir}/Floppy
%{_appsdir}/Floppy/*
%{_appsdir}/Floppy/.DirIcon

%dir %{_appsdir}/Floppy-2
%{_appsdir}/Floppy-2/*
%{_appsdir}/Floppy-2/.DirIcon

%dir %{_appsdir}/GZip
%{_appsdir}/GZip/*
%{_appsdir}/GZip/.DirIcon

%dir %{_appsdir}/xTerminal
%{_appsdir}/xTerminal/*
%{_appsdir}/xTerminal/.DirIcon


