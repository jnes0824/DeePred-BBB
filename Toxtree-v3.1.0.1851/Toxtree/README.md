java -jar Toxtree-3.1.0.1851.jar -n -i ../../fda.smi -o ../output/fda_bb_results.csv -m mutant.BB_CarcMutRules

java -jar Toxtree-3.1.0.1851.jar -n -i ../../fda.smi -o ../output/fda_ames_results.csv -m toxtree.plugins.ames.AmesMutagenicityRules

java -jar Toxtree-3.1.0.1851.jar -n -i ../../fda.smi -o ../output/fda_cramer_results.csv 



running
java -jar Toxtree-3.1.0.1851.jar -n -i ../../success_mols.smi -o ../output/success_mols_bb_results.csv -m mutant.BB_CarcMutRules

java -jar Toxtree-3.1.0.1851.jar -n -i ../../success_mols.smi -o ../output/success_mols_ames_results.csv -m toxtree.plugins.ames.AmesMutagenicityRules

java -jar Toxtree-3.1.0.1851.jar -n -i ../../success_mols.smi -o ../output/success_mols_cramer_results.csv 