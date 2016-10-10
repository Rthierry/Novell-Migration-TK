#!/usr/bin/ruby

#* ------------------------------------------------------ *#
#
#             - Script de conversion trustees NW vers OES -
#
#  * DESCRIPTION : Script de conversion des droits Netware
#					trustee.nlm vers rights Linux
# 
#  * AUTHOR: thierry.rangeard AT  netonline POINT fr
#  * CHANGELOG:
#        - 16-07-2009 : Creation
#      
#* ------------------------------------------------------ *#
# program: tn2l.rb
# usage:   ruby tn2l.rb tree_name vol_name InputFilename > OutputFilename

class Trights <
  Struct.new(:trustee, :path, :namespace, :usercn, :droits)

  def print_csv_record
    path.length==0 ? printf(",") : printf("\"%s\",", path)
    #trustee.length==0 ? printf(",") : printf("\"%s\",", trustee)
    #namespace.length==0 ? printf("") : printf("\"%s\"", namespace)
    droits.length==0 ? printf("") : printf("\"%s\"", droits)
    usercn.length==0 ? printf("") : printf("\"%s\"", usercn)
    printf("\n")
  end
end

#------#
# MAIN #
#------#

# bail out unless we get the right number of command line arguments
unless ARGV.length == 3
  puts "Man, not the right number of arguments."
  puts "Usage: ruby tn2l.rb InputFile.csv tree_name vol_name > linux_rights.sh\n"
  exit
end

# get the input filename from the command line
# get the tree name 
# get the destination vol name
input_file = ARGV[0]
tree_name = ARGV[1]
vol_name = "/media/nss/"+ARGV[2]

# define an array to hold the trustee records
arr = Array.new

# loop through each record in the csv file, adding
# each record to our array.
f = File.open(input_file, "r")
f.each_line { |line|
  words = line.split(',')
  p = Trights.new
  p.trustee = words[0].tr_s('"', '').strip
  p.path = words[1].gsub(/(.*:)/, vol_name)
  p.namespace = words[2].tr_s('"', '').strip
  p.usercn = words[3].insert -2, "."+tree_name
  p.droits = words[4].tr_s('"', '').strip.downcase
  arr.push(p)
}

# print out all the sorted records (just print to stdout)
arr.each { |p|
  puts 'rights -f "'+p.path.gsub(/\\/, '/')+' -r '+p.droits+' trustee '+p.usercn+"\n"
}