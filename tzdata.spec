Summary: Timezone data
Name: tzdata
Version: 2010l
%define tzdata_version 2010l
%define tzcode_version 2010l
Release: 1%{?dist}
License: Public Domain
Group: System Environment/Base
URL: ftp://elsie.nci.nih.gov/pub/

# The tzdata-base-0.tar.bz2 is a simple building infrastructure and
# a test suite.  It is occasionally updated from glibc sources, and as
# such is under LGPLv2+, but none of this ever gets to be part of
# final zoneinfo files.
Source0: tzdata-base-0.tar.bz2
# These are official upstream.
Source1: ftp://elsie.nci.nih.gov/pub/tzdata%{tzdata_version}.tar.gz
Source2: ftp://elsie.nci.nih.gov/pub/tzcode%{tzcode_version}.tar.gz
# __decl_patches
# __end

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: gawk, glibc, perl
BuildRequires: java-devel
BuildRequires: glibc-common >= 2.5.90-7
Conflicts: glibc-common <= 2.3.2-63
BuildArchitectures: noarch

%description
This package contains data files with rules for various timezones around
the world.

%package java
Summary: Timezone data for Java
Group: System Environment/Base
Source3: javazic.tar.gz
Patch0: javazic-fixup.patch

%description java
This package contains timezone information for use by Java runtimes.


%prep
%setup -q -n tzdata
mkdir tzdata%{tzdata_version}
tar xzf %{SOURCE1} -C tzdata%{tzdata_version}
mkdir tzcode%{tzcode_version}
tar xzf %{SOURCE2} -C tzcode%{tzcode_version}
sed -e 's|@objpfx@|'`pwd`'/obj/|' \
    -e 's|@datadir@|%{_datadir}|' \
  Makeconfig.in > Makeconfig
# __apply_patches
# __end

mkdir javazic
tar zxf %{SOURCE3} -C javazic
pushd javazic
%patch0

# Hack alert! sun.tools may be defined and installed in the
# VM. In order to guarantee that we are using IcedTea/OpenJDK
# for creating the zoneinfo files, rebase all the packages
# from "sun." to "rht.". Unfortunately, gcj does not support
# any of the -Xclasspath options, so we must go this route
# to ensure the greatest compatibility.
mv sun rht
find . -type f -name '*.java' -print0 \
    | xargs -0 -- sed -i -e 's:sun\.tools\.:rht.tools.:g' \
                         -e 's:sun\.util\.:rht.util.:g'
popd

%build
make
grep -v tz-art.htm tzcode%{tzcode_version}/tz-link.htm > tzcode%{tzcode_version}/tz-link.html

pushd javazic
javac -source 1.5 -target 1.5 -classpath . `find . -name \*.java`
popd
pushd tzdata%{tzdata_version}
java -classpath ../javazic/ rht.tools.javazic.Main -V %{version} \
  -d ../zoneinfo/java \
  africa antarctica asia australasia europe northamerica pacificnew \
  southamerica backward etcetera solar87 solar88 solar89 systemv \
  ../javazic/tzdata_jdk/gmt ../javazic/tzdata_jdk/jdk11_backward
popd

%install
rm -fr $RPM_BUILD_ROOT
sed -i 's|@install_root@|%{buildroot}|' Makeconfig
make install

cp -pr zoneinfo/java $RPM_BUILD_ROOT%{_datadir}/javazi

%check
echo ====================TESTING=========================
make check
echo ====================TESTING END=====================

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_datadir}/zoneinfo
%doc tzcode%{tzcode_version}/README
%doc tzcode%{tzcode_version}/Theory
%doc tzcode%{tzcode_version}/tz-link.html

%files java
%defattr(-,root,root)
%{_datadir}/javazi

%changelog
* Sun Jul 17 2011 Mike Adams <shalkie@gooseproject.org> - 2010l-1
- Initial rebuild for GoOSe Linux 6

* Mon Aug 30 2010 Petr Machata <pmachata@redhat.com> - 2010l-1
- Upstream 2010l:
  - Change Cairo's 2010 reversion to DST from the midnight between
    September 8 and 9 to the midnight between September 9 and 10.
  - Change Gaza's 2010 return to standard time to the midnight between
    August 10 and 11.
  - Bahia de Banderas (Mexican state of Nayarit) changed time zone
    UTC-7 to new time zone UTC-6 on April 4, 2010
- Resolves: #628645

* Tue Jul 27 2010 Andreas Schwab <schwab@redhat.com> - 2010k-1
- Upadate to 2010k (#618600)
  - No DST in Egypt during Ramadan in 2010
  - Bahía de Banderas moved to UTC-6 on April 4, 2010, new time zone
    America/Bahia_Banderas
  - Rename Pacific/Truk to Pacific/Chuuk and Pacific/Ponape to Pacific/Pohnpei
  - Update historical data of Europe/Helsinki
  - Update tz-links page

* Fri Apr 23 2010 Petr Machata <pmachata@redhat.com> - 2010i-1
- Upstream 2010i:
  - Morocco will have DST from 2010-05-02 to 2010-08-08
  - San Luis, Argentina will keep permanent DST after April 11, 2010
  - Updates of historical stamps for Taiwan
- Resolves: #585134 (Morocco starts DST on May 2, 2010)

* Tue Apr 06 2010 Petr Machata <pmachata@redhat.com> - 2010h-1
- Upstream 2009p
  - Argentina does not enter DST on October 18
  - San Luis switched from UTC-4 to UTC-3 on October 11th
- Upstream 2009q
  - Change DST end in Syria from November 1 to last Friday in October
  - Changes to past Hong Kong transitions
  - Kemerovo oblast' in Russia will change current time zone on March 28, 2010.
    Asia/Novokuznetsk is the new time zone name
- Upstream 2009r
  - Changes to local times of three Australian research stations in Antarctica
- Upstream 2009s
  - Fiji plans to re-introduce DST from November 29th 2009 to April 25th 2010
- Upstream 2009u
  - Bangladesh changed their clock back to Standard Time on December 31, 2009
- Upstream 2010a
  - Source code cleanups
- Upstream 2010b
  - Northern Mexico's border cities share the DST schedule with the
    United States
- Upstream 2010c
  - Paraguay DST now in effect from 2nd Sunday of April to 1st Sunday
    of October
- Upstream 2010d
  - The DST change in Bangladesh takes place a minute earlier
  - Fiji to end DST on 2010-03-28 at 03:00, about a month earlier
  - Samoa to observe DST this year; they didn't observe DST last year
  - DST in Chile extended to 3 April
- Upstream 2010e:
  - Fix a typo in Bangladesh DST rule
- Upstream 2010f:
  - Changes to Australian stations in Antarctica
  - Correct 2010 Samoa DST start date
  - New zone Antarctica/Macquarie
  - Change Syria DST start from last Friday in March to first Friday
    in April in 2010 and forward
- Upstream 2010g:
  - No Bangladesh DST in 2010 and forward.
  - Gaza DST starts last Saturday in March at 12:01 a.m. in 2010 and forward
  - Kamchatka and Anadyr change to Moscow+8 on 2010-03-28
  - Samara changes to Moscow+0 on 2010-03-28
  - Related zone.tab updates
- Upstream 2010h:
  - No DST in Tunisia in 2010 and forward
  - No DST in Pakistan in 2010 and forward
- Dropped tzdata-2009o-argentinas.patch
- Resolves: #568668 (DST time change in Paraguay [Asuncion])

* Wed Oct 21 2009 Petr Machata <pmachata@redhat.com> - 2009o-2
- San Luis (Argentina) entered DST on October 11 (tzdata-2009o-argentinas.patch)

* Mon Oct 19 2009 Petr Machata <pmachata@redhat.com> - 2009o-1
- Upstream 2009o
  - Bangladesh won't go back to Standard Time from October 1, 2009
  - Pakistan leaves DST on October 1, 2009
- Dropped tzdata-2009m-karachi.patch
- Argentina does not enter DST on October 18 (tzdata-2009o-argentinas.patch)

* Tue Sep 22 2009 Petr Machata <pmachata@redhat.com> - 2009m-2
- Add markers for autoupdate of spec file
- Pakistan leaves the period of DST on October 1 (tzdata-2009m-karachi.patch)

* Wed Sep 16 2009 Petr Machata <pmachata@redhat.com> - 2009m-1
- Upstream 2009m
  - Palestine will will revert back to winter time on Friday, 2009-09-04
  - Samoa passed the DST Bill that fixes DST dates for 2009 and 2010
- Drop Egypt patch

* Thu Aug 13 2009 Petr Machata <pmachata@redhat.com> - 2009k-3
- Egypt starts winter time on August 21.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009k-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Petr Machata <pmachata@redhat.com> - 2009k-1
- Upstream 2009k
  - Mauritius will not continue to observe DST the coming summer
  - Arbitrarily end DST at the end of 2009 so that a POSIX-style time
    zone string can appear in the Dhaka binary file

* Thu Jun 18 2009 Petr Machata <pmachata@redhat.com> - 2009j-1
- Upstream 2009j
  - DST switch for Bangladesh will occur an hour earlier than was
    thought.

* Mon Jun  8 2009 Petr Machata <pmachata@redhat.com> - 2009i-1
- Upstream 2009i
  - Bangladesh introduces DST 2009-06-20

* Tue May 26 2009 Petr Machata <pmachata@redhat.com> - 2009h-2
- Upstream 2009h
  - Convert use of 00:00 stamps to 24:00 of the previous day
  - Clarify that the data is Public Domain
- Drop Cairo patch

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009f-1
- Upstream 2009f
  - Pakistan will observe DST between 2009-04-15 and (probably) 2009-11-01
- Drop Pakistan patch

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009e-3
- Bump up for rebuild

* Mon Apr 13 2009 Petr Machata <pmachata@redhat.com> - 2009e-2
- Pakistan will observe DST between 2009-04-15 and (probably) 2009-11-01

* Mon Apr  6 2009 Petr Machata <pmachata@redhat.com> - 2009e-1
- Upstream 2009e
  - Historical changes for Jordan
  - Palestine will start DST on 2009-03-26 and end 2009-09-27
- Egypt ends DST on 2009-09-24

* Mon Mar 23 2009 Petr Machata <pmachata@redhat.com> - 2009d-1
- Upstream 2009d
  - Morocco will observe DST from 2009-06-01 00:00 to 2009-08-21 00:00
  - Tunisia will not observe DST this year.
  - Syria will start DST on 2009-03-27 00:00 this year
  - Cuba will start DST on midnight between 2009-03-07 and 2009-03-08
  - Province of San Luis, Argentina, went to UTC-04:00 on 2009-03-15

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2009a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Petr Machata <pmachata@redhat.com> - 2009a-1
- Upstream 2009a
  - Fix Asia/Kathmandu spelling
  - Historical timestamps for Switzerland and Cuba
  - DST update for America/Resolute

* Thu Oct 30 2008 Petr Machata <pmachata@redhat.com> - 2008i-1
- Upstream 2008i
  - Updates for Argentina: Drop DST in zones America/Argentina/Jujuy,
    La_Rioja, San_Juan, Catamarca, Mendoza, Rio_Gallegos, Ushuaia; new
    zone America/Argentina/Salta (for provinces SA, LP, NQ, RN).

* Mon Oct 13 2008 Petr Machata <pmachata@redhat.com> - 2008h-1
- Upstream 2008h
  - Fix exact DST transition hour for Mauritius
  - Syria will leave the period of DST on Nov 1
  - Fix coordinates of Pacific/Niue

* Tue Oct  7 2008 Petr Machata <pmachata@redhat.com> - 2008g-1
- Upstream 2008g
  - Fixed future DST transitions for Brazil

* Tue Sep 16 2008 Petr Machata <pmachata@redhat.com> - 2008f-1
- Upstream 2008f
  - Changes for Mauritius (extends DST to years to come)
  - Palestine changes clocks for the duration of Ramadan
  - Argentina will start DST on Sunday October 19, 2008
  - Brazil will start DST on 2008-10-19
- Drop Pakistan and Morocco patches

* Thu Aug 28 2008 Petr Machata <pmachata@redhat.com> - 2008e-2
- Pakistan DST is scheduled until Oct/31
- Morocco DST is scheduled until Aug/31

* Tue Aug 12 2008 Petr Machata <pmachata@redhat.com> - 2008e-1
- Upstream 2008e
  - Changes for Mauritius
  - Leap second coverage for 31/Dec 2008
  - Corrections of historical dates

* Tue Jul  8 2008 Petr Machata <pmachata@redhat.com> - 2008d-1
- Upstream 2008d
  - Changes for Brazil and Mauritius

* Wed May 30 2008 Petr Machata <pmachata@redhat.com> - 2008c-1
- Upstream 2008c
  - Mongolia changes zone
  - Pakistan DST is scheduled until Sep/1, instead of Aug/31
- Drop Morocco and Pakistan patches that are superseded by upstream
- Fix a typo in Java subpackage name

* Tue May 27 2008 Petr Machata <pmachata@redhat.com> - 2008b-3
- Morocco introduces DST

* Fri May 23 2008 Petr Machata <pmachata@redhat.com> - 2008b-2
- Pakistan introduces DST

* Wed Mar 26 2008 Petr Machata <pmachata@redhat.com> - 2008b-1
- Upstream 2008b
  - DST changes for Syria, Cuba; Iraq abandons DST
  - Saigon zone renamed Ho_Chi_Minh; backward link provided
  - Add America/Argentina/San_Luis information

* Tue Mar  4 2008 Petr Machata <pmachata@redhat.com> - 2007k-2
- Chile moves DST to 29/Mar
- Related: #435959

* Thu Jan  3 2008 Petr Machata <pmachata@redhat.com> - 2007k-1
- Upstream 2007k
  - Argentina readopted the daylight saving time

* Tue Dec  4 2007 Petr Machata <pmachata@redhat.com> - 2007j-1
- Upstream 2007j
  - New links America/St_Barthelemy and America/Marigot
  - Venezuela is changing their clocks on December 9 at 03:00

* Mon Nov  5 2007 Petr Machata <pmachata@redhat.com> - 2007i-1
- Upstream 2007i
  - Syria DST will take place at Midnight between Thursday and Friday.
  - Cuba will end DST on the last Sunday of October.
- Update tst-timezone.c from glibc CVS

* Mon Oct  1 2007 Petr Machata <pmachata@redhat.com> - 2007h-1
- Upstream 2007h
  - Brazil will observe DST from 2007-10-14 to 2008-02-17
  - Egypt and Gaza switched earlier than we expected
  - Iran will resume DST next year
  - Venezuela is scheduled to change TZ to -4:30 on January 1

* Thu Sep 25 2007 Keith Seitz <keiths@redhat.com> - 2007g-2
- Add support for building java's zoneinfo files in new
  tzdata-java RPM.

* Wed Aug 22 2007 Petr Machata <pmachata@redhat.com> - 2007g-1
- Fix licensing tag.
- Upstream 2007g
  - Egypt switches the September 7, not September 28
  - Daviess, Dubous, Knox, Martin, and Pike Counties, Indiana, switch
    from central to eastern time in November
  - South Australia, Tasmania, Victoria, New South Wales and Lord Howe
    Island are changing their DST rules effective next year
  - Sync several Antarctic station's rules with the New Zealand
  - leapseconds contain changes from the most recent IERS bulletin

* Wed May  9 2007 Petr Machata <pmachata@redhat.com> - 2007f-1
- Upstream 2007f
  - New Zealand is extending DST, starting later this year.
  - Haiti no longer observes DST.
  - The Turks and Caicos switch at 02:00, not at 00:00, and have
    adopted US DST rules.

* Tue Apr  3 2007 Petr Machata <pmachata@redhat.com> - 2007e-1
- Upstream 2007e
  - Syria switched to summer time at Mar/29.
  - Honduras will not enter DST this year.

* Wed Mar 21 2007 Petr Machata <pmachata@redhat.com> - 2007d-1
- Upstream 2007d
  - Mongolia has abolished DST.
  - Turkey will use EU rules this year, changing at 01:00 UTC rather
    than 01:00 standard time.
  - Cuba observed DST starting Sunday.
  - Resolute, Nunavut switched from Central to Eastern time last
    November.

* Mon Feb 26 2007 Petr Machata <pmachata@redhat.com> - 2007c-1
- Upstream 2007c
  - Pulaski County, Indiana, switched back to eastern time.
  - Turkey switches at 01:00 standard time, not at 01:00 UTC.
- Upstream 2007b
  - Changes to the commentary in "leapseconds".

* Wed Feb  7 2007 Petr Machata <pmachata@redhat.com> - 2007a-2
- tidy up the specfile per rpmlint comments

* Thu Jan 18 2007 Petr Machata <pmachata@redhat.com> - 2007a-1
- Upstream 2007a
  - Updates to Bahamas, they will be in sync with 2007 US DST change
  - New zone Australia/Eucla
  - Africa/Asmera renamed to Africa/Asmara, link created
  - Atlantic/Faeroe renamed to Atlantic/Faroe, link created
- Packaging
  - Adding BuildRequires: glibc-common >= 2.5.90-7 to build tzdata
    with extended 64-bit format necessary for dates beyond 2037

* Wed Nov 29 2006 Petr Machata <pmachata@redhat.com> - 2006p-1
- Upstream 2006p
  - Official version of Western Australia DST trial changes
  - Latitude/longitude changes for Europe/Jersey and Europe/Podgorica

* Wed Nov 22 2006 Petr Machata <pmachata@redhat.com> - 2006o-2
- Patch for Western Australia DST trial

* Thu Nov  9 2006 Petr Machata <pmachata@redhat.com> - 2006o-1
- Cuba has ended its three years of permanent DST.
- Updates in historical timestamps for Chile.

* Tue Oct 10 2006 Petr Machata <pmachata@redhat.com> - 2006m-2
- Proposed upstream patch (#210058)
  - Jordan will switch to winter time on October 27, not September 29
  - Brazil's DST this year is the first Sunday in November to the last
    Sunday in February.  (Thanks to Frederico A. C. Neves.)
  - ISO 3166 codes for Serbia and Montenegro, zone Europe/Podgorica
  - Commentary and past timestamps changes

* Tue Oct  3 2006 Petr Machata <pmachata@redhat.com> - 2006m-1
- Upstream 2006m:
  - Adjustments for Egypt, Palestine, Uruguay
  - Better description of `until' field in zic (8) manpage

* Thu Sep 21 2006 Petr Machata <pmachata@redhat.com> - 2006l-1
- Upstream 2006k, 2006l:
  - Adjustments for Egypt, Palestine, Cuba, Honduras
  - Documentation changes

* Tue Aug 22 2006 Petr Machata <pmachata@redhat.com> - 2006j-1
- Upstream 2006j
  - Honduras stopped observing DST on Monday at 00:00
  - America/Bermuda will follow the US's lead next year
  - America/Moncton will use US-style rules next year
  - New Zone America/Blanc-Sablon, for Canadians who observe AST all
    year
  - New zone: America/Atikokan instead of America/Coral_Harbour
  - New zones: Europe/Jersey, Europe/Guernsey, Europe/Isle_of_Man
  - Historical changes
  - Commentary updates
- Upstream 2006i
  - localtime.c fixes
- Upstream 2006h
  - zic leapsecond fix

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2006g-1.1
- rebuild

* Thu May 11 2006 Petr Machata <pmachata@redhat.com> - 2006g-1
- Honduras chose to follow Guatemala and will observe DST May/6 to Sep/2
- Nicaragua updates

* Tue May  2 2006 Petr Machata <pmachata@redhat.com> - 2006f-1
- Upstream 2006f
  - America/Guatemala observes DST between Apr/30 and Oct/1
  - Historical changes for Nicaragua
  - Update of America/Indiana/Vincennes in zone table

* Thu Apr 20 2006 Petr Machata <pmachata@redhat.com> - 2006d-1
- Upstream 2006d
  - Haiti observes DST
  - Sri Lanka change actually took effect Apr/15
  - All Canada is now scheduled for 2007 US DST rules
  - Some historical fixes

* Thu Apr  6 2006 Petr Machata <pmachata@redhat.com> - 2006c-1
- Upstream 2006c
  - Time-related changes:
    - dozens of historical and commentary changes
    - Iran stopped observing DST
    - Sri Lanka switches from UTC+6 to UTC+5:30
    - America/Thule and America/Edmonton will adopt new US rules,
      starting 2007
    - Tunisia is adopting regular DST
  - Code:
    - asctime.c: Chages in format strings to silent gcc warnings
    - removing K&R notation from function signatures
    - few fixes across the code

* Thu Mar 16 2006 Petr Machata <pmachata@redhat.com> - 2006b-2
- Patch for Sri Lanka time zone change (#184514)

* Thu Feb 22 2006 Petr Machata <pmachata@redhat.com> 2006b-1
- Upstream 2006b:
  - using tz64code version, as 32 is legacy according to tzdata ML
  - new manual pages for ctime, strftime, tzset
  - some source code reorganizations
  - no timezone/dst rule updates

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 2006a-2
- Small changes in tst-timezone.c

* Thu Feb 02 2006 Petr Machata <pmachata@redhat.com> 2006a-1
- Upstream 2006a:
  - private.h(scheck): changing char* to char const*
  - Rule changes for Palestine, zone changes for Indiana/US, both
    changes for Canada.
  - Many related doc changes.
- Naming scheme in spec file doesn't use %%{name}, but tzdata.

* Thu Jan 12 2006 Petr Machata <pmachata@redhat.com> 2005r-3
- 2005r-3
  - Meta changes.  Renaming tzdata.tar.bz2 file to tzdata$ver-base,
    so that it won't clash across updates.

* Thu Jan  5 2006 Petr Machata <pmachata@redhat.com> 2005r-2
- 2005r
  - Zones EST, MST, HST, EST5EDT, CST6CDT, MST7MDT, PST8PDT moved to
    northamerica to guard against old files with obsolete information
    being left in the time zone binary directory.
  - Changes for countries that are supposed to join 2007 US DST
    change.  This includes most of Canada, however entries already in
    the database (Alberta, British Columbia, Newfoundland, Northwest
    Territories, and Yukon) were left alone for the time being.
  - Fixes in zdump.c (abbrok): conditions are chained, and the string
    is checked for emptiness.

* Sat Dec 17 2005 Jakub Jelinek <jakub@redhat.com> 2005q-2
- 2005q
  - changes for Georgia, Azerbaijan, Jordan, Palestine, Cuba, Nicaragua
  - SystemV timezone changes

* Wed Nov  2 2005 Jakub Jelinek <jakub@redhat.com> 2005n-2
- 2005n
  - changes for Kyrgyzstan and Uruguay
- fix a typo in the Makefile (used TZDATA env var instead of TZDIR during
  make check), update tst-timezone.c from glibc CVS (#172102)

* Tue Sep  6 2005 Jakub Jelinek <jakub@redhat.com> 2005m-2
- 2005m
  - changes for USA (extending DST by 4 weeks since 2007), Tunisia,
    Australia, Kazakhstan
  - historical timezone data changes for Japan, Poland, Northern Ireland and
    Mali
  - timezone name change for East Timor

* Fri Jul 15 2005 Jakub Jelinek <jakub@redhat.com> 2005k-2
- 2005k
  - leap seconds update

* Sat Apr 30 2005 Jakub Jelinek <jakub@redhat.com> 2005i-2
- 2005i
  - updates for Iran, Haiti and Nicaragua

* Mon Apr  4 2005 Jakub Jelinek <jakub@redhat.com> 2005h-2
- 2005h
  - fixes for Kazakhstan

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 2005g-2
- 2005g
  - fixes for Uruguay
- include README and Theory from tzcode tarball in %%{_docdir};
  Theory includes a good summary of how the timezone data files
  are supposed to be named

* Tue Mar  1 2005 Jakub Jelinek <jakub@redhat.com> 2005f-2
- 2005f
  - more updates for Israel, updates for Azerbaijan

* Wed Jan 26 2005 Jakub Jelinek <jakub@redhat.com> 2005c-3
- 2005c
  - updates for Israel and Paraguay

* Mon Nov 29 2004 Jakub Jelinek <jakub@redhat.com> 2004g-1
- 2004g (#141107)
  - updates for Cuba

* Mon Oct 11 2004 Jakub Jelinek <jakub@redhat.com> 2004e-2
- 2004e (#135194)
  - updates for Brazil, Uruguay and Argentina

* Wed Aug  4 2004 Jakub Jelinek <jakub@redhat.com> 2004b-2
- 2004b

* Mon Oct  6 2003 Jakub Jelinek <jakub@redhat.com> 2003d-1
- 2003d

* Thu Sep 25 2003 Jakub Jelinek <jakub@redhat.com> 2003c-1
- 2003c
- updates for Brazil (#104840)

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2003a-2
- rebuilt

* Mon Jul 28 2003 Jakub Jelinek <jakub@redhat.com> 2003a-1
- initial package
