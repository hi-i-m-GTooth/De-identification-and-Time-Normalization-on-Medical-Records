cur_file=$(realpath "$0")
cur_dir=$(dirname "$cur_file")

bash $cur_dir/run_infer_ID.sh
echo "ID done"
bash $cur_dir/run_infer_TIME_ORG.sh
echo "TIME + ORG done"
bash $cur_dir/run_infer_RECORD_DOC.sh
echo "RECORD + DOC done"
bash $cur_dir/run_infer_DEP_PHONE_LOC.sh
echo "DEP + PHONE + LOC done"
bash $cur_dir/run_infer_CITY.sh
echo "CITY done"
bash $cur_dir/run_infer_STATE.sh
echo "STATE done"
bash $cur_dir/run_infer_ZIP.sh
echo "ZIP done"
bash $cur_dir/run_infer_DATE_DU.sh
echo "DATE + DURATION done"
bash $cur_dir/run_infer_HOS.sh
echo "HOSPITAL done"
bash $cur_dir/run_infer_AGE.sh
echo "AGE done"
bash $cur_dir/run_post.sh
echo "POST COUNTRY done"
echo "-- ALL DONE --"

bash $cur_dir/run_merge_ans.sh
