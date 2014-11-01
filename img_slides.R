library(png)
library(grid)
library(gridExtra)
library(ggplot2)

strats <- c("filt_global","filt_noglobal","nofilt_global","nofilt_noglobal")
derivatives <- c("reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd", 'vmhc', 
                 'dual_regression0', 'dual_regression1', 'dual_regression2','dual_regression3','dual_regression4', 
                 'dual_regression5','dual_regression6','dual_regression7','dual_regression8','dual_regression9')
pipes <- c("ccs", "cpac","dparsf","niak")

axials <- c()
saggitals <- c()

for (pipe in 1:length(pipes))
{
  pip <- pipes[pipe]
  pipstrats = paste0(pip,'_',strats)
  
  if (pip != "niak")
  {
    derivs <- c("falff","alff",derivatives)
  } else { derivs <- c("empty","empty", derivatives)}
  
  for (p in 1:length(pipstrats))
  {
    pipstrat = pipstrats[p]
    print (pipstrat)
    temp_axials <- c()
    temp_saggitals <- c()
    
    for (i in 1:length(derivs))
    {
      print (derivs[i])
      if (derivs[i] != "empty")
      {
        dir_name <- paste0("/home2/aimiwat/code/group_analysis/images/",pipstrat,"_",derivs[i])
      } else { dir_name <- "/home2/aimiwat/code/group_analysis/images/empty"}
      temp_axials = c(temp_axials,paste0(dir_name,"_axial.png"))
      temp_saggitals = c(temp_saggitals,paste0(dir_name,"_saggital.png"))
    }
    
    axials = rbind(axials,temp_axials)
    saggitals = rbind(saggitals, temp_saggitals)
  }
}
derivatives <- c("falff","alff","reho","degree_binarize","degree_weighted","eigenvector_weighted","eigenvector_binarize", "lfcd", 'vmhc', 
                 'dual_regression0', 'dual_regression1', 'dual_regression2','dual_regression3','dual_regression4', 
                 'dual_regression5','dual_regression6','dual_regression7','dual_regression8','dual_regression9')
height = 5
div = 34
left = 10
lmargin = 1
gp = gpar(fontsize = 18, col = "black")
blank_theme =   
  theme(
  line = element_blank(),
  axis.title = element_blank(),
  axis.text = element_blank(),
  panel.grid.major.x=element_blank(),
  panel.grid.major.y=element_blank(),
  plot.margin = unit(c(0,0,0,0),"cm"))

indexing <- function(p,s,d) {
  s+(p-1)*length(strats)+(d-1)*length(pipes)*length(strats)
}

for (d in 1:length(derivatives))
{
  for (s in 1:length(strats))
  {
  title = textGrob(derivatives[d], gp=gp)
  subtitle = textGrob(strats[s], gp=gp)
  
  #ccs
  p=1
  p_ccs <- qplot(1:40,1:40, geom="blank")+
    annotation_custom(textGrob("CCS", gp = gp), xmin = lmargin, xmax=left) +
    annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
    annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
    theme_bw()+
    blank_theme
  
  #cpac
  p=2
  p_cpac <- qplot(1:40,1:40, geom="blank")+
    annotation_custom(textGrob("CPAC", gp = gp), xmin = lmargin, xmax=left) +
    annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
    annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
    theme_bw()+
    blank_theme
  
  #dparsf
  p=3
  p_dparsf <- qplot(1:40,1:40, geom="blank")+
    annotation_custom(textGrob("DPARSF", gp = gp), xmin = lmargin, xmax=left) +
    annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
    annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
    theme_bw()+
    blank_theme
  
  #niak
  p=4
  p_niak <- qplot(1:40,1:40, geom="blank")+
    annotation_custom(textGrob("NIAK", gp = gp), xmin = lmargin, xmax=left) +
    annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
    annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
    theme_bw()+
    blank_theme
  
  filename = paste0("/home2/aimiwat/code/group_analysis/image_slides/by_pipeline/",derivatives[d],"_",strats[s],"_by_pipeline.png")
  print(filename)
  
  png(file=filename, width=11, height=8.5, units="in", res=300)
  grid.arrange(title, subtitle, p_ccs,p_cpac,p_dparsf, p_niak, heights=c(0.1,0.1,0.2,0.2,0.2,0.2),ncol=1)
  dev.off()
  }
  
  for (p in 1:length(pipes))
  {
    title = textGrob(derivatives[d], gp=gp)
    subtitle = textGrob(pipes[p], gp=gp)
    
    #filt_global
    s=1
    p_ccs <- qplot(1:40,1:40, geom="blank")+
      annotation_custom(textGrob("FILT_GLOBAL", gp = gp), xmin = lmargin, xmax=left) +
      annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
      annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
      theme_bw()+
      blank_theme
    
    #filt_noglobal
    s=2
    p_cpac <- qplot(1:40,1:40, geom="blank")+
      annotation_custom(textGrob("FILT_NOGLOBAL", gp = gp), xmin = lmargin, xmax=left) +
      annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
      annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
      theme_bw()+
      blank_theme
    
    #nofilt_global
    s=3
    p_dparsf <- qplot(1:40,1:40, geom="blank")+
      annotation_custom(textGrob("NOFILT_GLOBAL", gp = gp), xmin = lmargin, xmax=left) +
      annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
      annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
      theme_bw()+
      blank_theme
    
    #nofilt_noglobal
    s=4
    p_niak <- qplot(1:40,1:40, geom="blank")+
      annotation_custom(textGrob("NOFILT_NOGLOBAL", gp = gp), xmin = lmargin, xmax=left) +
      annotation_custom(rasterGrob(readPNG(axials[indexing(p,s,d)]), interpolate=TRUE), xmin=left, xmax=div) +
      annotation_custom(rasterGrob(readPNG(saggitals[indexing(p,s,d)]), interpolate=TRUE), xmin=div, xmax=40) +
      theme_bw()+
      blank_theme
    
    filename = paste0("/home2/aimiwat/code/group_analysis/image_slides/by_strategy/",derivatives[d],"_",pipes[p],"_by_strategy.png")
    print(filename)
    
    png(file=filename, width=11, height=8.5, units="in", res=300)
    grid.arrange(title, subtitle, p_ccs,p_cpac,p_dparsf, p_niak, heights=c(0.1,0.1,0.2,0.2,0.2,0.2),ncol=1)
    dev.off()
  }
}

#ggsave(filename=paste0("/home2/aimiwat/code/group_analysis/image_slides/",pipstrat,"img_slides_1.png"), plot=q, width=11, height=8.5, units="in")