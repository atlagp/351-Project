ls | while read -r d1 d2; do
git add $d1
git commit -m "converted $d1 "
git push
done
