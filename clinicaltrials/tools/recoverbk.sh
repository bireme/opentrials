dir=`dirname $0`;
for i in `ls -1 $dir/bkp`;
do
    appname=`cut -d'.' -f1 <<< $i`;
    target="$dir/../$appname/fixtures/initial_data.json";

    if [ -a "$target" ];
    then
        echo cp $dir/bkp/$i $target;
        cp $dir/bkp/$i $target;
    fi
done
echo ""
echo "Dont't forget to syncdb"
