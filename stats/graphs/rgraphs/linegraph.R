# Define the output file
output_file <- file.path(getwd(), "pdf/linegraph-heterogeneous.pdf")
pdf(output_file)

# Set the margins: mar = c(bottom, left, top, right)
par(mar = c(6, 7, 2, 1))

# Define x-axis points
xaxis=c(20,40,60,80)
# Set the margins: mgp
par(mgp = c(4, 1.5, 0))

# Define points
tf_het=c(94.20,90.21,78.82,75.22)
crh_het=c(99.73,99.40,99.72,99.17)
nexus_het=c(100,100,100,99.93)


plot( tf_het~xaxis,
      type="o", bty="o",
      xlab="Noise (%)",
      ylab="Avg. Accuracy (%)",
      col="black",
      lwd=5, pch=17, cex=3,
      ylim=c(75,100),
      cex.lab = 3,
      cex.axis = 2.5
    )

lines(crh_het ~xaxis,   col="black", lwd=5, cex=2.5, pch=16, type="o")
lines(nexus_het ~xaxis, col="black", lwd=5, cex=2.5, pch=15, type="o")

# Add a legend
legend("topright", 
       legend = c("TruthFinder", "CRH", "Nexus"), 
       col = c(
         "black", 
         "black", 
         "black"
        ), 
       lwd = 5,
       pch = c(17,16,15), 
       bty = "n", 
       pt.cex = 3.5, 
       cex = 2.25, 
       text.col = "black", 
       horiz = F , 
       inset = c(0.0, 0.1))

box(lwd = 3)

dev.off()