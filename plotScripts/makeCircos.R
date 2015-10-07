require(methods)
require(circlize)

###################
# Generate Circos #
###################
args<-commandArgs(TRUE)
bed<-args[1] #bed file 1

# Create dataframe from bed file
b<-read.delim(bed,header=FALSE,sep = "\t", dec=".")
chr1<-b[,1:3]
chr2<-b[,4:6]
score<-b[7]

# Print contents to stdout
print(b)
print(chr1)
print(chr2)
print(score)

# Plot chord diagram with hg19 cytoband ideogram
col_fun = colorRamp2(c(0,1),c("black","red") ,transparency = 0, space="RGB")
circos.par("track.height" = 0.1, cell.padding = c(0, 0, 0, 0))
circos.initializeWithIdeogram(cytoband = paste(system.file(package = "circlize"), "/extdata/cytoBand.txt", sep=""),species="hg19", track.height = 0.05, ideogram.height = 0.05)
circos.genomicLink(chr1, chr2, col= col_fun(unlist(score)), border = "black")
circos.clear()
#par(xpd= NA)
#plot(rep(1,nrow(b)), col=colorSelection, pch=19 , cex=3)# plot legend
