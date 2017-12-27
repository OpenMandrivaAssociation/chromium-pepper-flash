
NEWVER=`curl -s https://fpdownload.macromedia.com/pub/flashplayer/masterversion/masterversion.xml| grep -m 1 "linux"|cut -d '"' -f 2|sed -e "s/,/./g"`

sed -r -i "s/(Version:[[:space:]]{1,})([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})/\1$NEWVER/g" chromium-pepper-flash.spec

version=`grep ^Version chromium-pepper-flash.spec | awk '{print $2}'`
i386=`grep '^Source0:' chromium-pepper-flash.spec | sed "s|\%{version}|$version|g" | sed 's|^Source.:||g'`
x86_64=`grep '^Source1:' chromium-pepper-flash.spec | sed "s|\%{version}|$version|g" | sed 's|^Source.:||g'`
/bin/rm -f *.tar.gz
wget ${i386}
wget ${x86_64}


#for urlandno in $(grep "^\%define downurl" chromium-pepper-flash.spec | grep -v \%nil | awk '{print substr($2,length($2),1) "|" $3}')
#do

#   IFS="|" read -a myarray <<< "$urlandno"

#   url=${myarray[1]}
#   no=${myarray[0]}

#   occ=1
#   echo $url | grep x86_64
#   if [ $? -eq 0 ]; then
#      occ=2
#   fi

#   fin=`echo $url | sed -e "s/%{version}/$version/g"`

#   file=`basename $fin`

#   wget $fin
#   sum=`sha256sum $file | awk '{print $1}'`

#   fsize=`stat --printf="%s" $file`

#   echo $fsize
   #define tsha256sum1     a4b229470e62fedcd7edbf5cdf2bb90f8f43f1a6fa5286240e35433d7c73a125:6918554

#   if [ $occ -eq 1 ]; then
#     sed -i "s/ tsha256sum${no}.*/ tsha256sum${no}\t$sum:$fsize/" chromium-pepper-flash.spec
#   else
#     sed -i "0,/ tsha256sum${no}.*/! s/ tsha256sum${no}.*/ tsha256sum${no}\t$sum:$fsize/" chromium-pepper-flash.spec
#   fi
#   rm -f $file
#done
