library(ggplot2)
library(reshape2)
library(plyr)

derivs <- c("falff","alff","reho","degree_binarize","degree_weighted","eigen_vector_weighted","lfcd")
corrs <- c("concordance","pearson","spearmans","entropy")

for (i in 1:length(derivs))
{
  for (j in 1:length(corrs))
  {
    deriv_file <- paste0("/home/rschadmin/abide/spat_corr_", derivs[i],"_",corrs[j],".csv")
    print(deriv_file)
    ddata <- read.csv(deriv_file, header=T)
  
    ddata.m <- melt(ddata)
    ddata.m <- ddply(ddata.m, .(variable), transform)
    
    base_size <- 16
    
    png_file = paste0("/home/rschadmin/abide/spat_plot_",derivs[i],"_",corrs[j],".png")
    
    p = ggplot(ddata.m, aes(variable, X)) + 
         geom_tile(aes(fill=value), colour = "white") + 
         scale_fill_gradient(limits=c(0,1),low = "white", high = "steelblue") + 
         theme_grey(base_size = base_size) + labs(x = "", y = "") + 
         #scale_x_discrete(expand = c(0, 0)) +
         #scale_y_discrete(expand = c(0, 0)) + 
         ylim(rev(sort(levels(ddata.m$variable)))) + 
         xlim(levels(ddata.m$X)) +
         theme(legend.position = "right", axis.ticks = element_blank(), axis.text.x = element_text(size = base_size * 0.8, angle = 330, hjust = 0, colour = "grey50"))
    
    ggsave(filename=png_file, plot=last_plot())
  }
}
