start=`date +%s.%N`
Rscript SPiPv2.1_main.r -I spip_4k.txt -O spip_4k_out.txt
end=`date +%s.%N`

runtime=$( echo "$end - $start" | bc -l )
echo "Runtime was $runtime seconds"
