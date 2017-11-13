#!/usr/bin/perl
#title           : groupmember.pl
#description     :
#author          : Maxime MENGUAL
#date            :
#version         : 1.0
#usage           : perl
#notes           : Perl standard Library
use strict;
use warnings;
### File name is given as the first argument
my $groupFile = $ARGV[0]; ### The file containing the HID is given as the first argument
### Name of CSV export
my $groupExport = "$groupFile.csv";
### Open trustee export file and write header
open(FIC,">$groupExport") or die("open: $!");
open my $fh, $groupFile or die "Could not open $groupFile :$! ";
print FIC "\"fqdn\",\"group\",\"member\"\n";
my $group;
my $fqdngroup;
while( my $line = <$fh>)  {
        if ( $line =~ m/dn:\ (.*)/ )
        {
                $fqdngroup=$1;
        }
        if ( $line =~ m/dn:\ [cC][nN]=([^,]*).*/ )
        {
                $group = $1;
                print FIC "\"$fqdngroup\",\"$group\",\"\"\n";
        }
        if ( $line =~ m/member:\ [cC][nN]=([^,]*).*/ ){
                print FIC "\"$fqdngroup\",\"$group\",\"$1\"\n";
        }
}
close $fh;
