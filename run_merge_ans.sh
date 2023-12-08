cur_file=$(realpath "$0")
cur_dir=$(dirname "$cur_file")

# Grep the patterns in the files and merge the results
merged_output=${cur_dir}/final_submissions/merged_output.txt
touch $merged_output
grep -E $'\tIDNUM\t' ${cur_dir}/final_submissions/splitAll_ID/answer.txt >> $merged_output
grep -E $'\tPATIENT\t|\tSTREET\t' ${cur_dir}/final_submissions/1prefix_410m_5prefix_PAT_STR/answer.txt >> $merged_output
grep -E $'\tZIP\t' ${cur_dir}/final_submissions/160m_retry1_ZIP/answer.txt >> $merged_output
grep -E $'\tSTATE\t' ${cur_dir}/final_submissions/160m_retry3_STATE/answer.txt >> $merged_output
grep -E $'\tAGE\t' ${cur_dir}/final_submissions/160m_retry5_AGE/answer.txt >> $merged_output
grep -E $'\tMEDICALRECORD\t|\tDOCTOR\t' ${cur_dir}/final_submissions/160m_retry6_RECORD_DOC/answer.txt >> $merged_output
grep -E $'\tHOSPITAL\t' ${cur_dir}/final_submissions/160m_retry7_HOS/answer.txt >> $merged_output
grep -E $'\tTIME\t|\tORGANIZATION\t' ${cur_dir}/final_submissions/160m_retry9_TIME_ORG/answer.txt >> $merged_output
grep -E $'\tDEPARTMENT\t|\tPHONE\t|\tLOCATION-OTHER\t' ${cur_dir}/final_submissions/410m_DEP_PHONE_LOC/answer.txt >> $merged_output
grep -E $'\tCITY\t' ${cur_dir}/final_submissions/De_410m_aug_ep20_CITY/answer.txt >> $merged_output
grep -E $'\tDATE\t|\tDURATION\t' ${cur_dir}/final_submissions/Norm_410m_aug_20ep_DATE_DU/answer.txt >> $merged_output
cat ${cur_dir}/final_submissions/COUNTRY_POST/answer.txt >> $merged_output

echo "Merged output # of lines: $(wc -l $merged_output)"

# Sort, remove duplicates lines. Then remove lines with less than 5 columns.
sort $merged_output | uniq | awk "NF>=5" > ${cur_dir}/final_submissions/result/answer.txt 
echo "Final answer # of lines: $(wc -l ${cur_dir}/final_submissions/result/answer.txt)"
rm $merged_output
