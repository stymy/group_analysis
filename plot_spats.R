library(ggplot2)
library(reshape2)
library(plyr)
library(gridExtra)

labels_corr <- list(scale_y_continuous(limits=c(0,1))
                      #facet_grid(strategy1_filt + strategy2_filt ~ strategy1_global + strategy2_global)
                    )

theme_corr <- theme(plot.title = element_text(hjust=1),
                    axis.text.x = element_blank(),#element_text(angle=45, hjust=1),
                    axis.title.x = element_blank(),
                    axis.ticks.x = element_blank(),
                    legend.position = "none",
                    panel.grid.minor.x=element_blank(),
                    panel.grid.minor.y=element_blank(),
                    strip.text = element_text(size=6))

df_all= data.frame(row.names=NULL)

derivs <- c("dual_regression9", "dual_regression8", "dual_regression7", "dual_regression6","dual_regression5","dual_regression4","dual_regression3","dual_regression2","dual_regression1","dual_regression0","lfcd","eigenvector_binarize","eigenvector_weighted","degree_binarize","degree_weighted","vmhc","falff","alff","reho")
#derivs <- c("falff","alff","reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd", "vmhc", 'dual_regression0', 'dual_regression1', "dual_regression2", "dual_regression3", "dual_regression4", "dual_regression5", "dual_regression6", "dual_regression7", "dual_regression8", "dual_regression9") 
corrs <- c("concordance","pearson","dice","spearmans")#,"entropy")
strats <- c("filt_global","filt_noglobal","nofilt_global","nofilt_noglobal")
pipes <- "cpac"
pipstrats = paste0(pipes,'_',strats)
s = combn(pipstrats,2)
pipstrat_list = apply(s,2,paste,collapse="_v_")

j = 0
i = 0
p = 0

for (j in 1:length(corrs)) 
{
  print (corrs[j])
  for (p in 1:length(pipstrat_list))
  { 
    pipstrat = pipstrat_list[p]
    pipstrat1 = s[1,p]
    pipstrat2 = s[2,p]
    print (pipstrat)
    for (i in 1:length(derivs))
    {
      print (derivs[i])
      #boot_file <- paste0("/home/rschadmin/abide/bootstraps_", pipstrat, "/boot_",derivs[i],".csv")
      #null_file <- paste0("/home/rschadmin/abide/nullstraps_", pipstrat, "/null_",derivs[i],".csv")
      
      #bdata <- read.csv(boot_file, header=T)
      #ndata <- read.csv(null_file, header=T)

      deriv_file <- paste0("/home/rschadmin/Soft/group_analysis/spat_corr_16_", derivs[i],"_",corrs[j],".csv")
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
        strategy = paste(strsplit(pipstrat1,'_')[[1]][2], strsplit(pipstrat1,'_')[[1]][3],'and',strsplit(pipstrat2,'_')[[1]][2], strsplit(pipstrat2,'_')[[1]][3]),
        #strategy1_filt = strsplit(pipstrat1,'_')[[1]][2],
        #strategy1_global = strsplit(pipstrat1,'_')[[1]][3],
        #strategy2_filt = strsplit(pipstrat2,'_')[[1]][2],
        #strategy2_global = strsplit(pipstrat2,'_')[[1]][3],
        #null = sapply(ndata[corrs[j]], mean),
        #null_err = sapply(bdata[corrs[j]], sd),
        corr = measured_corr,
        corr_type = corrs[j],
        #boot = sapply(bdata[corrs[j]], mean),
        #boot_err = sapply(bdata[corrs[j]], sd),
        row.names=NULL
      )
      #limits <- aes(ymax = boot + boot_err, ymin=boot - boot_err)
      
      df_all <- rbind(df, df_all)
    }
  }
}

j = 0
for (j in 1:length(corrs)) 
{
  corr_data <- subset(df_all, subset=corr_type==corrs[j])
  
  p_ccs <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    ggtitle("CCS") +
    #geom_pointrange(limits) +
    geom_point() +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    ylab(corrs[j])+
    theme_corr
  
  p_cpac <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    ggtitle("CPAC") +
    #geom_pointrange(limits) +
    geom_point() +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    theme_corr +
    theme_bw()+
    ylab(corrs[j])+
    theme_corr
  
  p_dparsf <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    ggtitle("DPARSF") +
    #geom_pointrange(limits) +
    geom_point() +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    ylab(corrs[j])+
    theme_corr
  
  p_niak <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    ggtitle("NIAK") +
    #geom_pointrange(limits) +
    geom_point() +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    ylab(corrs[j])+
    theme_corr
  
  p_derivs <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    geom_point(color="white")+
    labels_corr+
    theme_bw()+
    #theme_corr+
    theme(plot.background = element_blank(),
          panel.border = element_blank(),
          axis.text.y = element_text(colour="white"),
          axis.text.x = element_text(angle=45, hjust=1),
          axis.title = element_text(colour="white"),
          axis.ticks = element_blank(),
          line = element_blank())
  
  p_legend <-ggplot(data=corr_data, aes(y=corr, color=strategy, x=derivative)) +
    geom_point()+
    labels_corr+
    theme_bw()+
    #theme_corr+
    theme(plot.background = element_blank(),
          panel.border = element_blank(),
          axis.text = element_blank(),
          axis.title = element_blank(),
          axis.ticks = element_blank(),
          line = element_blank(),
          legend.position = "bottom",
          legend.direction = "vertical",
          legend.title=element_blank(),
          legend.key=element_rect(color="white"))+
    guides(colour = guide_legend(nrow = 2))
  
    ggsave(filename=paste0(corr[j],"plot.png"), plot=p_cpac)
  
  png(file = paste0("/home/rschadmin/Soft/group_analysis/plots/",corrs[j],"_plot.png"), width=8.5, height=11, units="in", res=300)
  grid.arrange(p_ccs,p_cpac,p_dparsf, p_niak, p_derivs, p_legend, heights=c(0.2,0.2,0.2,0.2,0.1,0.1),ncol=1)
  dev.off()
}
