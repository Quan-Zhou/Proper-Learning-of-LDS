#!/bin/sh
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --error=/home/zhouqua1/NCPOP/err.err 
#SBATCH --output=/home/zhouqua1/NCPOP/out.out 
#SBATCH --mem-per-cpu 64G
#SBATCH --time 1-00:00:00 
#SBATCH --partition=amd

ml mosek/9.2
ml Python/3.9.6-GCCcore-11.2.0
#ml Julia/1.8.5-linux-x86_64

python /home/zhouqua1/NCPOP/ncpop_stock.py
#julia /home/zhouqua1/NCPOP/stock_nctssos.jl
#python /home/zhouqua1/NCPOP/ncpop100.py
#python /home/zhouqua1/NCPOP/ncpop300.py
#python /home/zhouqua1/NCPOP/ncpop_parameters.py
#python /home/zhouqua1/NCPOP/ncpop_momentdegree.py
#python /home/zhouqua1/NCPOP/ncpop300.py
#python /home/zhouqua1/NCPOP/ncpop100_higherorder.py
#python /home/zhouqua1/NCPOP/ncpop300_higherorder.py
#python /home/zhouqua1/NCPOP/ncpop300_higherdim.py
