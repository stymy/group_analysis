library(ggplot2)
library(reshape2)
library(plyr)
library(gridExtra)

labels_corr <- list(scale_y_continuous(limits=c(0,1)), scale_x_discrete(drop=FALSE))

theme_corr <- theme(plot.title = element_text(hjust=1, face="bold"),
                    axis.text.x = element_blank(),
                    axis.title.x = element_blank(),
                    axis.ticks.x = element_blank(),
                    axis.title.y = element_text(size=8),
                    axis.ticks.y = element_blank(),
                    axis.text.y = element_text(size=6),
                    panel.border = element_blank(),
                    legend.position = "none",
                    panel.grid.minor.x=element_blank(),
                    panel.grid.major.y=element_blank(),
                    strip.text = element_text(size=6))

df_all= data.frame(row.names=NULL)

derivs <- c("dual_regression9", "dual_regression8", "dual_regression7", "dual_regression6","dual_regression5","dual_regression4","dual_regression3","dual_regression2","dual_regression1","dual_regression0","lfcd","eigenvector_binarize","eigenvector_weighted","degree_binarize","degree_weighted","vmhc","reho","falff","alff")
#derivs <- c("falff","alff","reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd", "vmhc", 'dual_regression0', 'dual_regression1', "dual_regression2", "dual_regression3", "dual_regression4", "dual_regression5", "dual_regression6", "dual_regression7", "dual_regression8", "dual_regression9") 
corrs <- c("concordance","spearmans","entropy","dice","pearson")
strats <- c("filt_global","filt_noglobal","nofilt_global","nofilt_noglobal")
pipelines <- c("cpac", "dparsf","niak","ccs")
for (pip in 1:length(pipelines))
{
  pipes <- pipelines[pip]
  pipstrats = paste0(pipes,'_',strats)
  s = combn(pipstrats,2)
  pipstrat_list_orig = apply(s,2,paste,collapse="_v_")
  pipstrat_list = c()
  for (pip2 in 1:length(pipelines))
  {
    pipes2 <- pipelines[pip2]
    pipstrat_list = rbind(pipstrat_list, c( paste0(pipes,"_filt_noglobal_v_",pipes2,"_nofilt_global"),
                     paste0(pipes,"_filt_global_v_",pipes2,"_nofilt_noglobal"),
                     
                     paste0(pipes,"_filt_noglobal_v_",pipes2,"_nofilt_noglobal"),
                     paste0(pipes,"_filt_global_v_",pipes2,"_nofilt_global"),
                     
                     paste0(pipes,"_nofilt_global_v_",pipes2,"_nofilt_noglobal"),
                     paste0(pipes,"_filt_global_v_",pipes2,"_filt_noglobal")
                    ))
  }
  
  j = 0
  i = 0
  p = 0
  
  for (j in 1:length(corrs)) 
  {
    print (corrs[j])
    for (p in 1:length(pipstrat_list))
    { 
      pipstrat = pipstrat_list[p]
      pipstrat1 = strsplit(pipstrat,'_v_')[[1]][1]
      pipstrat2 = strsplit(pipstrat,'_v_')[[1]][2]
      print (pipstrat)
      for (i in 1:length(derivs))
      {
        print (derivs[i])
        #boot_file <- paste0("/home/rschadmin/abide/bootstraps_", pipstrat, "/boot_",derivs[i],".csv")
        #null_file <- paste0("/home/rschadmin/abide/nullstraps_", pipstrat, "/null_",derivs[i],".csv")
        
        #bdata <- read.csv(boot_file, header=T)
        #ndata <- read.csv(null_file, header=T)
  
        deriv_file <- paste0("/home/rschadmin/Soft/group_analysis/spat_corr_", derivs[i],"_",corrs[j],".csv")
        ddata <- read.csv(deriv_file, header=T, row.names=1)

        measured_corr = ddata[pipstrat1,pipstrat2]
        
        if (length(measured_corr) !=0)
        {
          df <- data.frame(
            pipeline = paste(strsplit(pipstrat1,'_')[[1]][1],'and',strsplit(pipstrat2,'_')[[1]][1]),
            strategy = paste0(strsplit(pipstrat1,'_')[[1]][2], '_', strsplit(pipstrat1,'_')[[1]][3],' and ',strsplit(pipstrat2,'_')[[1]][2],'_',strsplit(pipstrat2,'_')[[1]][3]),
            derivative = c(derivs[i]),
            pipstrategy = paste(strsplit(pipstrat1,'_')[[1]][2], strsplit(pipstrat1,'_')[[1]][3],'and',strsplit(pipstrat2,'_')[[1]][2], strsplit(pipstrat2,'_')[[1]][3]),
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
  }
}
  
j = 0
for (j in 1:length(corrs)) 
{
  corr_data <- subset(df_all, subset=corr_type==corrs[j])
  
  p_ccs <-ggplot(data=subset(corr_data, subset=pipeline=="ccs and ccs"), aes(y=corr, color=pipstrategy, x=derivative)) +
    ggtitle("CCS") +
    #geom_pointrange(limits) +
    geom_point(alpha=0.5, size=4, shape=15) +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+  
    scale_colour_brewer(palette="Paired")+
    ylab(corrs[j])+
    theme_corr
  
  p_cpac <-ggplot(data=subset(corr_data, subset=pipeline=="cpac and cpac"), aes(y=corr, color=pipstrategy, x=derivative)) +
    ggtitle("CPAC") +
    #geom_pointrange(limits) +
    geom_point(alpha=0.5, size=4, shape=15) +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    scale_colour_brewer(palette="Paired")+
    ylab(corrs[j])+
    theme_corr
  
  p_dparsf <-ggplot(data=subset(corr_data, subset=pipeline=="dparsf and dparsf"), aes(y=corr, color=pipstrategy, x=derivative)) +
    ggtitle("DPARSF") +
    #geom_pointrange(limits) +
    geom_point(alpha=0.5, size=4, shape=15) +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    scale_colour_brewer(palette="Paired")+
    ylab(corrs[j])+
    theme_corr
  
  p_niak <-ggplot(data=subset(corr_data, subset=pipeline=="niak and niak"), aes(y=corr, colour=pipstrategy, x=derivative)) +
    ggtitle("NIAK") +
    #geom_pointrange(limits) +
    geom_point(alpha=0.5, size=4, shape=15) +
    #geom_hline(aes(yintercept=sapply(df_all['null']+df_all['null_err'],mean)), size=0.2, alpha=0.3, linetype="dashed") +
    labels_corr+
    theme_bw()+
    scale_colour_brewer(palette="Paired")+
    ylab(corrs[j])+
    theme_corr
  
  p_derivs <-ggplot(data=corr_data, aes(y=corr, colour=pipstrategy, x=derivative)) +
    geom_point(alpha=0.5,size=3, shape=15)+#color="white")+
    labels_corr+
    theme_bw()+
    scale_colour_brewer(palette="Paired")+
    #theme_corr+
    theme(plot.background = element_blank(),
          panel.border = element_blank(),
          axis.text.y = element_text(colour="white"),
          axis.text.x = element_text(angle=45, hjust=1, size=12, face="bold"),
          axis.title = element_text(colour="white"),
          axis.ticks = element_blank(),
          line = element_blank(),
          legend.position = "bottom",
          legend.direction = "vertical",
          legend.title=element_blank(),
          legend.key=element_rect(color="white"))+
    guides(colour = guide_legend(nrow = 2))
  
  png(file = paste0("/home/rschadmin/Soft/group_analysis/plots/",corrs[j],"_plot.png"), width=8.5, height=11, units="in", res=300)
  grid.arrange(p_ccs,p_cpac,p_dparsf, p_niak, p_derivs, heights=c(0.2,0.2,0.2,0.2,0.2),ncol=1)
  dev.off()
}