tn=7
python3 -m unittest discover > testout.txt 2>&1
out=`tail -1 testout.txt`
if [ "$out" = "OK" ]
then
  echo FS_SCORE:100%
elif [ "$(echo testout.txt | grep failures)" = "" ]
then
  echo FS_SCORE:0%
else
  out=`echo $out | sed 's/failures=/\n/g' | tail -1`
  tf=`echo $out | cut -c1-1`
  FS_SCORE=`awk -v tests_failed="$tf" -v tests_total="$tn" 'BEGIN {print (tests_total - tests_failed) / tests_total * 100}'`
  echo "FS_SCORE:$FS_SCORE%"
fi