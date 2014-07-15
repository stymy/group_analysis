library(png)
library(grid)

derivs <- c("falff","alff","reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd")#, 'vmhc', 'dual_regression'
corrs <- c("concordance","pearson","dice","entropy","spearmans")
strats <- c("filt_global","filt_noglobal","nofilt_global","nofilt_noglobal")
pipes <- "cpac"
pipstrats = paste0(pipes,'_',strats)

for (p in 1:length(pipstrats))
{
  pipstrat = pipstrats[p]
  print (pipstrat)
  axials = c()
  saggitals= c()
  
  for (i in 1:length(derivs))
  {
    print (derivs[i])
    dir_name <- paste0("/home/rschadmin/abide/images/",pipstrat,"_",derivs[i])
    axials[i] = paste0(dir_name,"_axial.png")
    saggitals[i]=paste0(dir_name,"_saggital.png")
  }
  height = 5
  div = 34
  left = 10
  lmargin = 1
  gp = gpar(fontsize = 12, col = "white")
  
  q <- qplot(1:40,1:40, geom="blank")+
    geom_ribbon(aes(ymin=0, ymax=40), fill="black") +
    #falff
    annotation_custom(textGrob("FALFF", gp = gp), xmin = lmargin, xmax=left, ymin=35, ymax=40) +
    annotation_custom(rasterGrob(readPNG(axials[1]), interpolate=TRUE), xmin=left, xmax=div, ymin=35, ymax=40) +
    annotation_custom(rasterGrob(readPNG(saggitals[1]), interpolate=TRUE), xmin=div, xmax=40, ymin=35, ymax=40) +
    #alff
    annotation_custom(textGrob("ALFF", gp = gp), xmin = lmargin, xmax=left, ymin=30, ymax=35) +
    annotation_custom(rasterGrob(readPNG(axials[2]), interpolate=TRUE), xmin=left, xmax=div, ymin=30, ymax=35) +
    annotation_custom(rasterGrob(readPNG(saggitals[2]), interpolate=TRUE), xmin=div, xmax=40, ymin=30, ymax=35) +
    #reho
    annotation_custom(textGrob("REHO", gp = gp), xmin = lmargin, xmax=left, ymin=25, ymax=30) +
    annotation_custom(rasterGrob(readPNG(axials[3]), interpolate=TRUE), xmin=left, xmax=div, ymin=25, ymax=30) +
    annotation_custom(rasterGrob(readPNG(saggitals[3]), interpolate=TRUE), xmin=div, xmax=40, ymin=25, ymax=30) +
    #degree_binarize
    annotation_custom(textGrob("DEGREE\nBINARIZED", gp = gp), xmin = lmargin, xmax=left, ymin=20, ymax=25) +
    annotation_custom(rasterGrob(readPNG(axials[4]), interpolate=TRUE), xmin=left, xmax=div, ymin=20, ymax=25) +
    annotation_custom(rasterGrob(readPNG(saggitals[4]), interpolate=TRUE), xmin=div, xmax=40, ymin=20, ymax=25) +
    #degree_weighted
    annotation_custom(textGrob("DEGREE\nWEIGHTED", gp = gp), xmin = lmargin, xmax=left, ymin=15, ymax=20) +
    annotation_custom(rasterGrob(readPNG(axials[5]), interpolate=TRUE), xmin=left, xmax=div, ymin=15, ymax=20) +
    annotation_custom(rasterGrob(readPNG(saggitals[5]), interpolate=TRUE), xmin=div, xmax=40, ymin=15, ymax=20) +
    #eigenvector_binarize
    annotation_custom(textGrob("EIGENECTOR\nBINARIZED", gp = gp), xmin = lmargin, xmax=left, ymin=10, ymax=15) +
    annotation_custom(rasterGrob(readPNG(axials[7]), interpolate=TRUE), xmin=left, xmax=div, ymin=10, ymax=15) +
    annotation_custom(rasterGrob(readPNG(saggitals[7]), interpolate=TRUE),xmin=div, xmax=40, ymin=10, ymax=15) +
    #eigenvector_weighted
    annotation_custom(textGrob("EIGENVECTOR\nWEIGHTED", gp = gp), xmin = lmargin, xmax=left, ymin=5, ymax=10) +
    annotation_custom(rasterGrob(readPNG(axials[6]), interpolate=TRUE), xmin=left, xmax=div, ymin=5, ymax=10) +
    annotation_custom(rasterGrob(readPNG(saggitals[6]), interpolate=TRUE), xmin=div, xmax=40, ymin=5, ymax=10) +
    #lfcd
    annotation_custom(textGrob("LFCD", gp = gp), xmin = lmargin, xmax=left, ymin=0, ymax=5) +
    annotation_custom(rasterGrob(readPNG(axials[8]), interpolate=TRUE), xmin=left, xmax=div, ymin=0, ymax=5) +
    annotation_custom(rasterGrob(readPNG(saggitals[8]), interpolate=TRUE), xmin=div, xmax=40, ymin=0, ymax=5) +
    theme_bw()+
    theme(
      line = element_blank(),
      axis.title = element_blank(),
      axis.text = element_blank(),
      panel.grid.major.x=element_blank(),
      panel.grid.major.y=element_blank(),
      plot.margin = unit(c(0,0,0,0),"cm")
    )
  ggsave(filename=paste0("/home/rschadmin/abide/images/",pipstrat,"img_summaries.png"), plot=q)
}
