library(ggplot2)
library(reshape2)
library(plyr)


df_all= data.frame(row.names=NULL)


derivs <- c("falff","alff","reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd", "vmhc", 'dual_regression0', 'dual_regression1', "dual_regression2", "dual_regression3", "dual_regression4", "dual_regression5", "dual_regression6", "dual_regression7", "dual_regression8", "dual_regression9") 
corrs <- c("concordance","pearson","dice","entropy","spearmans")
strats <- c("filt_global","filt_noglobal","nofilt_global","nofilt_noglobal")
pipes <- "cpac"
pipstrats = paste0(pipes,'_',strats)
s = combn(pipstrats,2)
pipstrat_list = apply(s,2,paste,collapse="_v_")

for (p in 1:length(pipstrat_list))
{
  pipstrat = pipstrat_list[p]
  pipstrat1 = s[1,p]
  pipstrat2 = s[2,p]
  print (pipstrat)
  for (i in 1:length(derivs))
  {
    print (derivs[i])
    boot_file <- paste0("/home/rschadmin/abide/bootstraps_", pipstrat, "/boot_",derivs[i],".csv")
    null_file <- paste0("/home/rschadmin/abide/nullstraps_", pipstrat, "/null_",derivs[i],".csv")
    
    bdata <- read.csv(boot_file, header=T)
    ndata <- read.csv(null_file, header=T)
    
    for (j in 1:length(corrs)) 
    {
      print (corrs[j])
      deriv_file <- paste0("/home/rschadmin/Soft/group_analysis/spat_corr_", derivs[i],"_",corrs[j],".csv")
      ddata <- read.csv(deriv_file, header=T, row.names=1)
      if (corrs[j]=="dice")
      {
        measured_corr = ddata[2,pipstrat]
      }
      else{
        measured_corr = ddata[pipstrat2,pipstrat1]
      }
      df <- data.frame(
        derivative = c(derivs[i]),
        strategy1_filt = strsplit(pipstrat1,'_')[[1]][2],
        strategy1_global = strsplit(pipstrat1,'_')[[1]][3],
        strategy2_filt = strsplit(pipstrat2,'_')[[1]][2],
        strategy2_global = strsplit(pipstrat2,'_')[[1]][3],
        null = sapply(ndata[corrs[j]], mean),
        null_err = sapply(bdata[corrs[j]], sd),
        corr = measured_corr,
        corr_type = corrs[j],
        boot = sapply(bdata[corrs[j]], mean),
        boot_err = sapply(bdata[corrs[j]], sd),
        row.names=NULL
      )
      limits <- aes(ymax = boot + boot_err, ymin=boot - boot_err)
      
      df_all <- rbind(df, df_all)
    }
  }
}
p <-ggplot(data=df_all, aes(y=corr, color=corr_type, x=derivative)) +
  geom_pointrange(limits) +
  geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
  scale_y_continuous(limits=c(0,1)) +
  facet_grid(strategy1_filt + strategy2_filt ~ strategy1_global + strategy2_global) +
  theme(axis.text.x = element_text(angle=90),
        axis.ticks.x = element_blank(),
        panel.grid.major.x=element_blank(),
        panel.grid.minor.y=element_blank(),
        strip.text = element_text(size=6))

ggsave(filename="plot.png", plot=p)
